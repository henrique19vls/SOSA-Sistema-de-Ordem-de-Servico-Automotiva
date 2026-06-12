# SOSA — Sistema de Ordem de Serviço Automotiva

Sistema de gerenciamento de ordens de serviço para oficinas mecânicas, desenvolvido em Python com banco de dados MySQL, simulando o funcionamento de um sistema corporativo real.

---

## Tecnologias

- Python 3.11+
- MySQL 8.x
- mysql-connector-python

---

## Funcionalidades

- Cadastro de clientes com validação de unicidade
- Abertura de ordens de serviço por tipo de serviço e veículo
- Encaminhamento de ordens para mecânicos com base em urgência e gravidade
- Classificação automática de prioridade (Baixa, Média ou Alta)
- Conclusão de atendimentos com registro de solução aplicada
- Histórico completo de ordens finalizadas
- Estatísticas com totais por status e por prioridade (via SQL)
- Consultas por prioridade e por cliente

---

## Estrutura do Banco de Dados

| Tabela           | Descrição                                          |
|------------------|----------------------------------------------------|
| `clientes`       | Clientes que podem abrir ordens de serviço         |
| `mecanicos`      | Mecânicos responsáveis pelos atendimentos          |
| `tipos_servico`  | Tipos de serviço disponíveis na oficina            |
| `ordens_servico` | Ordens abertas, em manutenção e finalizadas        |
| `historico`      | Registro de ordens concluídas com solução aplicada |

---

## Fluxo do Sistema

1. **Cadastrar cliente** — registra cliente com nome e telefone (unicidade validada)
2. **Registrar ordem** — cliente seleciona tipo de serviço e descreve o problema
3. **Encaminhar ordem** — define urgência e gravidade, calcula prioridade e atribui mecânico
4. **Concluir ordem** — mecânico registra a solução e finaliza o atendimento
5. **Ver histórico** — exibe todas as ordens finalizadas com detalhes
6. **Ver estatísticas** — resumo por status, por prioridade e consultas por filtro

---

## Regra de Prioridade

A prioridade é calculada automaticamente com base em uma matriz de urgência × gravidade, onde a urgência tem peso maior:

| Urgência \ Gravidade | Leve  | Moderada | Grave |
|----------------------|-------|----------|-------|
| Baixa                | Baixa | Baixa    | Média |
| Média                | Média | Média    | Alta  |
| Alta                 | Alta  | Alta     | Alta  |

- **Prioridade Baixa** → estagiário e auxiliar de mecânico
- **Prioridade Média** → mecânico e auxiliar de mecânico
- **Prioridade Alta** → mecânico chefe e mecânico

A regra é determinística: as mesmas entradas sempre resultam na mesma prioridade. A prioridade é calculada no momento do encaminhamento e salva no banco para consultas futuras.

---

## Regra de Transição de Status

As ordens seguem o fluxo: `aberta` → `em manutencao` → `finalizada`

- Uma ordem só pode ser encaminhada se estiver com status `aberta`
- Uma ordem só pode ser concluída se estiver com status `em manutencao`
- Ordens finalizadas não podem ser reabertas ou encaminhadas novamente

---

## Como Executar

### 1. Instalar dependências

```bash
pip install mysql-connector-python
```

### 2. Configurar a conexão

Abra `database.py` e altere a senha:

```python
password="sua_senha_aqui"
```

### 3. Criar o banco de dados

Execute o script SQL no MySQL:

```bash
mysql -u root -p < banco.sql
```

Ou abra o arquivo `banco.sql` no MySQL Workbench e execute.

### 4. Rodar o sistema

```bash
python main.py
```

---

## Estrutura dos Arquivos

```
├── database.py  # configuração da conexão com o MySQL
├── funcoes.py   # funções principais do sistema
├── main.py      # menu e inicialização do sistema
└── banco.sql    # script de criação do banco de dados
```

---

## Autor

- Henrique Bortolo Nascimento — RA: 26005457
