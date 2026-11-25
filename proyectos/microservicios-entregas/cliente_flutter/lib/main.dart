import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

/// Base del gateway. Ejemplos:
/// - Web en la misma máquina: http://127.0.0.1:8080
/// - Emulador Android: http://10.0.2.2:8080
/// - Escritorio en la misma red: http://127.0.0.1:8080
const String kApiBase = String.fromEnvironment(
  'API_BASE',
  defaultValue: 'http://127.0.0.1:8080',
);

void main() {
  runApp(const EntregasApp());
}

class EntregasApp extends StatelessWidget {
  const EntregasApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Entregas — cliente',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF1F4E79)),
        useMaterial3: true,
      ),
      home: const PedidoPage(),
    );
  }
}

class PedidoPage extends StatefulWidget {
  const PedidoPage({super.key});

  @override
  State<PedidoPage> createState() => _PedidoPageState();
}

class _PedidoPageState extends State<PedidoPage> {
  final _formKey = GlobalKey<FormState>();
  bool _enviando = false;
  String? _mensaje;
  Map<String, dynamic>? _respuesta;

  final _distancia = TextEditingController(text: '12.64');
  final _peso = TextEditingController(text: '0.31');
  final _largo = TextEditingController(text: '11.7');
  final _ancho = TextEditingController(text: '7.6');
  final _alto = TextEditingController(text: '10.6');
  final _volumen = TextEditingController(text: '0.94');
  final _valor = TextEditingController(text: '4603');
  final _hora = TextEditingController(text: '3');

  String _prioridad = 'mismo_dia';
  String _zona = 'periferia';
  String _clima = 'despejado';
  String _trafico = 'medio';
  int _fragil = 0;
  int _refrigerado = 0;

  @override
  void dispose() {
    for (final c in [
      _distancia,
      _peso,
      _largo,
      _ancho,
      _alto,
      _volumen,
      _valor,
      _hora,
    ]) {
      c.dispose();
    }
    super.dispose();
  }

  Map<String, dynamic> _paquete() {
    return {
      'distancia_km': double.parse(_distancia.text),
      'peso_kg': double.parse(_peso.text),
      'largo_cm': double.parse(_largo.text),
      'ancho_cm': double.parse(_ancho.text),
      'alto_cm': double.parse(_alto.text),
      'volumen_l': double.parse(_volumen.text),
      'fragil': _fragil,
      'refrigerado': _refrigerado,
      'valor_declarado_mxn': double.parse(_valor.text),
      'prioridad': _prioridad,
      'zona_destino': _zona,
      'clima': _clima,
      'hora_salida': int.parse(_hora.text),
      'trafico': _trafico,
    };
  }

  Future<void> _enviar() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _enviando = true;
      _mensaje = null;
      _respuesta = null;
    });
    try {
      final uri = Uri.parse('$kApiBase/pedidos');
      final r = await http.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(_paquete()),
      );
      final cuerpo = jsonDecode(r.body);
      setState(() {
        _respuesta = cuerpo is Map<String, dynamic> ? cuerpo : {'raw': cuerpo};
        _mensaje = r.statusCode == 201
            ? 'Pedido creado (HTTP ${r.statusCode})'
            : 'Respuesta HTTP ${r.statusCode}';
      });
    } catch (e) {
      setState(() {
        _mensaje = 'No hubo respuesta del gateway ($kApiBase): $e';
      });
    } finally {
      setState(() => _enviando = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final medio = _respuesta?['medio']?.toString();
    return Scaffold(
      appBar: AppBar(
        title: const Text('Entregas — microservicios'),
        bottom: PreferredSize(
          preferredSize: const Size.fromHeight(28),
          child: Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: Text(
              'API_BASE=$kApiBase',
              style: Theme.of(context).textTheme.bodySmall,
            ),
          ),
        ),
      ),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Text(
              'Cliente Flutter del demo. Envía POST /pedidos al gateway '
              '(pedidos → recomendar).',
              style: Theme.of(context).textTheme.bodyMedium,
            ),
            const SizedBox(height: 16),
            Wrap(
              spacing: 12,
              runSpacing: 12,
              children: [
                _num('Distancia km', _distancia),
                _num('Peso kg', _peso),
                _num('Largo cm', _largo),
                _num('Ancho cm', _ancho),
                _num('Alto cm', _alto),
                _num('Volumen L', _volumen),
                _num('Valor MXN', _valor),
                _num('Hora salida', _hora, entero: true),
              ],
            ),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              initialValue: _prioridad,
              decoration: const InputDecoration(labelText: 'Prioridad'),
              items: const [
                DropdownMenuItem(value: 'mismo_dia', child: Text('mismo_dia')),
                DropdownMenuItem(value: 'normal', child: Text('normal')),
              ],
              onChanged: (v) => setState(() => _prioridad = v ?? _prioridad),
            ),
            DropdownButtonFormField<String>(
              initialValue: _zona,
              decoration: const InputDecoration(labelText: 'Zona'),
              items: const [
                DropdownMenuItem(value: 'periferia', child: Text('periferia')),
                DropdownMenuItem(value: 'centro', child: Text('centro')),
              ],
              onChanged: (v) => setState(() => _zona = v ?? _zona),
            ),
            DropdownButtonFormField<String>(
              initialValue: _clima,
              decoration: const InputDecoration(labelText: 'Clima'),
              items: const [
                DropdownMenuItem(value: 'despejado', child: Text('despejado')),
                DropdownMenuItem(value: 'lluvia', child: Text('lluvia')),
              ],
              onChanged: (v) => setState(() => _clima = v ?? _clima),
            ),
            DropdownButtonFormField<String>(
              initialValue: _trafico,
              decoration: const InputDecoration(labelText: 'Tráfico'),
              items: const [
                DropdownMenuItem(value: 'bajo', child: Text('bajo')),
                DropdownMenuItem(value: 'medio', child: Text('medio')),
                DropdownMenuItem(value: 'alto', child: Text('alto')),
              ],
              onChanged: (v) => setState(() => _trafico = v ?? _trafico),
            ),
            SwitchListTile(
              title: const Text('Frágil'),
              value: _fragil == 1,
              onChanged: (v) => setState(() => _fragil = v ? 1 : 0),
            ),
            SwitchListTile(
              title: const Text('Refrigerado'),
              value: _refrigerado == 1,
              onChanged: (v) => setState(() => _refrigerado = v ? 1 : 0),
            ),
            const SizedBox(height: 12),
            FilledButton(
              onPressed: _enviando ? null : _enviar,
              child: Text(_enviando ? 'Enviando…' : 'Crear pedido'),
            ),
            if (_mensaje != null) ...[
              const SizedBox(height: 16),
              Text(_mensaje!, style: Theme.of(context).textTheme.titleMedium),
              if (medio != null)
                Text('Medio sugerido: $medio',
                    style: Theme.of(context).textTheme.headlineSmall),
              if (_respuesta != null)
                Padding(
                  padding: const EdgeInsets.only(top: 8),
                  child: SelectableText(
                    const JsonEncoder.withIndent('  ').convert(_respuesta),
                    style: const TextStyle(fontFamily: 'monospace', fontSize: 12),
                  ),
                ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _num(String label, TextEditingController c, {bool entero = false}) {
    return SizedBox(
      width: 160,
      child: TextFormField(
        controller: c,
        decoration: InputDecoration(labelText: label),
        keyboardType: const TextInputType.numberWithOptions(decimal: true),
        validator: (v) {
          if (v == null || v.isEmpty) return 'Requerido';
          if (entero) return int.tryParse(v) == null ? 'Entero' : null;
          return double.tryParse(v) == null ? 'Número' : null;
        },
      ),
    );
  }
}
