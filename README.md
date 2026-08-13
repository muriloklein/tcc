# ROADMAP

## Etapa 1 — Seleção e pré-processamento dos dados
**Prazo da proposta: julho → 1ª semana de agosto**

- Selecionar cenários do IoT-23 com PortScan, DDoS e Okiru + os 3 cenários de tráfego benigno ✅
- Remover atributos identificadores (IPs, timestamps brutos) e campos com risco de data leakage ✅
- Tratar valores ausentes/inconsistentes, codificar atributos categóricos, normalizar atributos numéricos ✅
- Analisar exploratoriamente a distribuição de classes (confirmar o desbalanceamento: PortScan e Okiru majoritários) ✅
- Decidir entre SMOTE, `class_weight='balanced'`, ou combinação — avaliado empiricamente sobre o conjunto de treino ✅
  *(decisão final: SMOTE só na tarefa binária; multiclasse usa class_weight, por conta de okiru/ddos)*

**Correções adicionais feitas dentro da Etapa 1** (não previstas na proposta original, mas necessárias):
- Descoberta e correção de 40,2% de duplicatas exatas causando vazamento treino/teste ✅
- Inversão da ordem do pipeline de amostragem (deduplicar por classe ANTES do CAP_POR_CLASSE) para preservar diversidade real de classes com tráfego repetitivo (okiru: 2 → 621 linhas únicas) ✅

## Etapa 2 — Divisão dos dados e definição da tarefa
**Prazo: início de agosto (junto com o fim da Etapa 1)**

- Split estratificado 70/30 (treino/teste) ✅
- Preparar as duas configurações de classificação: binária (benigno vs. malicioso) e multiclasse (por tipo de ataque) ✅
- Sobreposição treino/teste confirmada em 0 após as correções ✅

## Etapa 3 — Implementação dos modelos
**Prazo: agosto → outubro**

- Random Forest (binário + multiclasse, class_weight e SMOTE onde aplicável) ✅
- SVM (binário + multiclasse, class_weight e SMOTE onde aplicável) ✅
- Árvore de Decisão (binário + multiclasse, class_weight e SMOTE onde aplicável) ✅
- CNN (Keras + TensorFlow), incluindo o reshape dos atributos tabulares em formato matricial com zero-padding 🔜

## Etapa 4 — Ajuste de hiperparâmetros
**Prazo: outubro → novembro**

- Modelos clássicos: Grid Search + validação cruzada estratificada de 5 folds ⬜
- CNN: Random Search restrito + holdout + early stopping (sem CV completa, por custo computacional) ⬜

## Etapa 5 — Avaliação e comparação estatística
**Prazo: novembro → dezembro**

- Calcular acurácia, precisão, recall, F1-Score e tempo de inferência no conjunto de teste ⬜
- Para RF/SVM/AD: métricas como média ± desvio padrão dos 5 folds ⬜
- Para CNN: 5 execuções independentes com seeds diferentes (mesma arquitetura/hiperparâmetros) ⬜
- Teste de Wilcoxon (α = 0,05) pareado entre os modelos ⬜
- Gráficos comparativos e matrizes de confusão ⬜
  *(já temos as matrizes de confusão individuais de RF/SVM/AD multiclasse - reaproveitar)*

## Redação final e defesa
**Prazo: em paralelo às etapas finais → defesa em dezembro**

- Texto final incorporando os resultados de cada etapa ⬜
- Não esquecer a Seção 4.4 (Limitações e ameaças à validade) — já está escrita na proposta, só revisar à luz dos resultados reais
  *(pontos já identificados para incluir: duplicatas extremas em okiru/ddos, separabilidade quase perfeita específica a este recorte de cenários, sensibilidade do SVM a ddos sem tuning)*