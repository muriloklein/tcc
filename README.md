# ROADMAP

## Etapa 1 — Seleção e pré-processamento dos dados
**Prazo da proposta: julho → 1ª semana de agosto**

- Selecionar cenários do IoT-23 com PortScan, DDoS e Okiru + os 3 cenários de tráfego benigno
- Remover atributos identificadores (IPs, timestamps brutos) e campos com risco de data leakage
- Tratar valores ausentes/inconsistentes, codificar atributos categóricos, normalizar atributos numéricos
- Analisar exploratoriamente a distribuição de classes (confirmar o desbalanceamento: PortScan e Okiru majoritários)
- Decidir entre SMOTE, `class_weight='balanced'`, ou combinação — avaliado empiricamente sobre o conjunto de treino

## Etapa 2 — Divisão dos dados e definição da tarefa
**Prazo: início de agosto (junto com o fim da Etapa 1)**

- Split estratificado 70/30 (treino/teste)
- Preparar as duas configurações de classificação: binária (benigno vs. malicioso) e multiclasse (por tipo de ataque)

## Etapa 3 — Implementação dos modelos
**Prazo: agosto → outubro**

- Random Forest, SVM e Árvore de Decisão (Scikit-learn) — ago/set
- CNN (Keras + TensorFlow), incluindo o reshape dos atributos tabulares em formato matricial com zero-padding — set/out

## Etapa 4 — Ajuste de hiperparâmetros
**Prazo: outubro → novembro**

- Modelos clássicos: Grid Search + validação cruzada estratificada de 5 folds
- CNN: Random Search restrito + holdout + early stopping (sem CV completa, por custo computacional)

## Etapa 5 — Avaliação e comparação estatística
**Prazo: novembro → dezembro**

- Calcular acurácia, precisão, recall, F1-Score e tempo de inferência no conjunto de teste
- Para RF/SVM/AD: métricas como média ± desvio padrão dos 5 folds
- Para CNN: 5 execuções independentes com seeds diferentes (mesma arquitetura/hiperparâmetros)
- Teste de Wilcoxon (α = 0,05) pareado entre os modelos
- Gráficos comparativos e matrizes de confusão

## Redação final e defesa
**Prazo: em paralelo às etapas finais → defesa em dezembro**

- Texto final incorporando os resultados de cada etapa (os commits do GitHub viram um bom guia de "o que aconteceu quando")
- Não esquecer a Seção 4.4 (Limitações e ameaças à validade) — já está escrita na proposta, só revisar à luz dos resultados reais