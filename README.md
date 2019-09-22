# TokenGraph
Method of ranking token importance in raw text using cooccurrence scores and embedded vector similarity of token definitions to build weighted, directed graph of token relationships. Iterative ranking can be run over a subgraph of frequency-weighted tokens until convergence to re-rank tokens and  identify those that are relevant but not present. Outputs of this process dataset are used as targets for ML.