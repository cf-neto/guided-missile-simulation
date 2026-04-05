# Guided Missile Simulation

Simulação 2D de um míssil guiado perseguindo um alvo em movimento, renderizada em tempo real com **Python** e **Matplotlib**.

---

## Descrição

O míssil é lançado verticalmente (fase de *boost*) e, em seguida, orienta-se dinamicamente em direção ao alvo com guiagem direta baseada em vetores normalizados. O alvo se move de forma autônoma, trocando de destino aleatoriamente a cada 2 segundos. A simulação encerra automaticamente ao detectar colisão.

---

## Classes e Lógica

### `Target`
Representa o alvo em movimento.

| Atributo | Valor padrão | Descrição |
|---|---|---|
| `speed` | `3` | Velocidade de movimento |
| `change_interval` | `40 frames` | Intervalo para trocar de destino (~2s) |

- Move-se em direção a um destino aleatório dentro do campo `[0, 300]`
- A cada 40 frames, sorteia um novo destino
- Usa vetor de direção normalizado para movimento suave

### `Rocket`
Representa o míssil com duas fases de voo.

| Atributo | Valor padrão | Descrição |
|---|---|---|
| `acceleration` | `0.15` | Aceleração por frame |
| `max_speed` | `2.8` | Velocidade máxima |
| `boost_height` | `50` | Altura da fase de lançamento vertical |

**Fase `boost`:** lançamento vertical até atingir 50 unidades de altura.  
**Fase `guidance`:** guiagem ativa em direção ao alvo com recálculo a cada frame.

Colisão detectada quando: `distância ao alvo < velocidade atual`

---

## Como Executar
 
**Pré-requisito:** Python 3.14.3
 
```bash
# Clonar o repositório
git clone https://github.com/cf-neto/guided-missile-simulation.git
cd guided-missile-simulation
 
# Instalar dependências
pip install -r requirements.txt
 
# Rodar a simulação
python main.py
```

Uma janela gráfica abrirá com a simulação em tempo real.

---

## Parâmetros Configuráveis

Você pode ajustar os parâmetros diretamente no `main.py`:

```python
target = Target(250, 200)          # Posição inicial do alvo
rocket = Rocket(25, 0)             # Posição inicial do míssil

# Dentro das classes:
self.speed = 3                     # Velocidade do alvo
self.change_interval = 40          # Frequência de mudança de direção

self.acceleration = 0.15           # Aceleração do míssil
self.max_speed = 2.8               # Velocidade máxima do míssil
self.boost_height = 50             # Altura do boost inicial
```

---

## Tecnologias

- **Python 3.14.3**
- **Matplotlib** — renderização e animação
- **math** — cálculo de distâncias euclidianas
- **random** — geração de destinos aleatórios

---

## Possíveis Melhorias

- [ ] Guiagem proporcional (*Proportional Navigation*)
- [ ] Física com gravidade e resistência do ar
- [ ] Suporte a múltiplos alvos simultâneos
- [ ] Exportar simulação como GIF ou MP4
- [ ] Interface para ajuste de parâmetros em tempo real

---

## Licença

Este projeto está sob a licença MIT.
