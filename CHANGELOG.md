# Changelog

## v0.5.0 - Julho/2026

### 🚀 Motor de Geração

- Implementação do motor CP-SAT utilizando Google OR-Tools.
- Nova arquitetura modular do motor.
- Separação entre motor guloso e CP-SAT.
- Implementação das restrições obrigatórias.
- Implementação da função objetivo.
- Implementação do solver.
- Implementação do extrator de solução.
- Implementação do diagnóstico inicial.

### 📈 Resultado

- 1.080 variáveis de decisão.
- 120 aulas alocadas automaticamente.
- Primeira geração completa de grade utilizando CP-SAT.

### 🔧 Arquitetura

- Criação da pasta `services/motor/cp_sat`.
- Preservação do motor guloso para comparação de desempenho.