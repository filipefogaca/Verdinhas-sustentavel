# 📈 Plano de Projeto: Verdinhas (Versão Final)

Este documento detalha a estratégia de escalabilidade, infraestrutura de hardware e o planejamento financeiro para a implementação do ecossistema Verdinhas em larga escala.

## 1. Escopo da Versão Final
Diferente do protótipo funcional atual, a versão final foca em automação total do descarte e segurança na geração de pontos.

* **Lixeiras Inteligentes:** Unidades de descarte equipadas com sensores IoT para validação de resíduos.
* **QR Code Dinâmico:** Geração de códigos únicos em displays físicos após a confirmação do peso e tipo de material.
* **App Mobile:** Aplicativo nativo para usuários gerenciarem cashback e localizarem pontos de coleta via GPS.

## 2. Estimativa de Investimento (100 Unidades)

Para uma implementação municipal ou corporativa, o investimento inicial (CapEx) é detalhado abaixo:

| Item | Descrição | Custo Unitário | Total (100 Unid.) |
| :--- | :--- | :--- | :--- |
| **Hardware IoT** | ESP32, Sensores (Peso/Nível) e Display | R$ 225,00 | R$ 22.500,00 |
| **Estrutura** | Corpo em metal/plástico e Painel Solar | R$ 600,00 | R$ 60.000,00 |
| **Mão de Obra** | Montagem e Calibração | R$ 75,00 | R$ 7.500,00 |
| **Logística** | Frete e Instalação Física | R$ 100,00 | R$ 10.000,00 |
| **TOTAL** | | **R$ 1.000,00** | **R$ 100.000,00** |

## 3. Infraestrutura Tecnológica (Tech Stack Final)
* **Servidores:** Migração para nuvem (AWS/Azure) para gestão de dados em tempo real.
* **Inteligência:** Modelos de Machine Learning (Scikit-learn) para prever rotas de coleta otimizadas com base no nível de preenchimento das lixeiras.
* **BI:** Dashboards no Power BI para monitoramento de KPIs ambientais e saúde do hardware.

## 4. O que o Protótipo já entrega
* **Backend Flask:** Gestão de rotas, usuários e lógica de pontuação.
* **Banco de Dados:** Estrutura inicial para armazenamento de transações.
* **Storytelling Interativo:** Apresentação de impactos para investidores e gestores públicos.
