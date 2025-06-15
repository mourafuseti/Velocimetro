# Velocímetro de Internet

Um aplicativo em Python que simula um velocímetro de internet, inspirado no SpeedTest, com interface gráfica usando Pygame. O programa testa a velocidade de download e upload, exibe pings e IPs de sites como globo.com, google.com, youtube.com e o DNS 8.8.8.8, e apresenta um velocímetro com ponteiro suave.

## Criador
- **Nome**: Leonardo de Moura Fuseti
- **Email**: mourafuseti@hotmail.com

## Funcionalidades
- **Velocímetro**: Exibe a velocidade de download com um ponteiro que se move suavemente de 0 a 100 Mbps, com arco gradiente (verde a vermelho).
- **Teste de Velocidade**: Usa a biblioteca `speedtest-cli` para medir download e upload, com simulação de resultados em ambientes sem suporte (como Pyodide).
- **Pings e IPs**: Mostra pings (em milissegundos inteiros) e IPs resolvidos para globo.com, google.com, youtube.com e 8.8.8.8.
- **Interface Gráfica**: Inclui um botão "Iniciar" com efeito de hover, caixas estilizadas para pings/IPs, e um título centralizado.
- **Layout**: Velocímetro posicionado à direita e acima, resultados de velocidade e botão abaixo, caixas de ping/IP à esquerda.

## Requisitos
- Python 3.7+
- Bibliotecas Python:
  - `pygame`
  - `speedtest-cli`
  - `ping3`
- Para execução no Pyodide (navegador), as bibliotecas `speedtest-cli` e `ping3` podem não funcionar, usando simulação com valores aleatórios.

## Instalação
1. Clone o repositório ou baixe o arquivo `speedtest.py`.
2. Instale as dependências:
   ```bash
   pip install pygame speedtest-cli ping3
   ```
3. Execute o script:
   ```bash
   python speedtest.py
   ```

## Como Usar
1. Execute o programa (`python speedtest.py`).
2. A interface mostra:
   - Velocímetro à direita e acima.
   - Caixas de ping/IP à esquerda (globo.com, google.com, youtube.com, 8.8.8.8).
   - Resultados de download e upload abaixo do velocímetro.
   - Botão "Iniciar" abaixo dos resultados.
3. Clique no botão "Iniciar" para começar o teste.
4. Durante o teste (5 segundos):
   - A agulha do velocímetro se move suavemente, indicando a velocidade de download.
   - Após o teste, os resultados finais de download e upload são exibidos.
5. Pings e IPs são atualizados ao iniciar o programa.

## Notas
- **Pyodide**: Em ambientes de navegador (Pyodide), `speedtest-cli` e `ping3` podem não funcionar devido a restrições de rede. O programa usa valores aleatórios simulados.
- **Teste Local**: Para resultados reais, execute localmente com as bibliotecas instaladas.
- **Personalização**: O código pode ser modificado para ajustar posições, cores ou adicionar mais sites.

## Licença
Este projeto é licenciado sob a Licença MIT. Veja o arquivo [LICENSE](#) para detalhes.

---

Desenvolvido por Leonardo de Moura Fuseti (mourafuseti@hotmail.com).