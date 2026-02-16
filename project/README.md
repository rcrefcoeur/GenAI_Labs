# Improving atropinesterase solubility using …
## Introduction
Atropine is an alkaloid toxin produced by plants in the nightshade family, particularly Atropa belladonna (deadly nightshade), Datura stramonium (jimsonweed), and Mandragora officinarum (mandrake).  They produce it as a way of defense against insects and herbivores. Plants producing atropine may grow in between agricultural crops, and end up in harvested produce, such as cereals. At that point it is no longer easily separated, and a too high atropine concentration means the harvest is no longer valid for human consumption, thus leading to economic loss. 

<div style="background-color: white; display: inline-block; padding: 4px;">
  <img src="images/Atropine.svg" width="350" alt="Atropine structure">
</div>

(https://commons.wikimedia.org/wiki/File:Atropine.svg)

Medically, atropine is used as an antagonist to muscarinic acetylcholine receptors, and as an antidote in case of poisoning by sarin, a highly lethal nerve agent. Between the late 1950s and early 1980s, in the midst of the cold war, many nations were stockpiling large amounts of sarin, fueling the interest in atropine and its enzymatic degradation. Some soil bacteria have evolved with the ability to degrade and use atropine as a carbon (and some even as nitrogen) source. A strain of *P.putida* was found to have an atropinesterase enzyme, catalyzing the hydrolysis of atropine into tropine and tropic acid (Rörsch *et al.* 1971). The peptide sequence was established by Edman degradation. By the time genomics and proteomics techniques were commonplace, the research interest in atropinesterases had already dissipated, resulting in the absence of curated genomic sequences of atropinesterases in present databases.

Atropinesterases are part of a broader family of enzymes, the alpha/beta hydrolases. Distinctive for this class of enzymes is the catalytic triad, consisting of three distinct amino acids: a nucleophile, an acid, and a base (Bartholomew *et al.* 1996). In a recent project I experimentally characterized the *Pseudomonas putida* atropinesterase, and confirmed its atropinesterase activity. By homology search, five more atropinesterase homologs were identified.

During these experiments, it was observed that all atropinesterases were prone to form aggregates, which is a major cause for activity loss. Enhancing the solubility of enzymes is one method to reduce aggregate formation, thus improving their longevity. Among the evaluated homologs, Acinetobacter tandoii atropinesterase had the highest activity. The objective of this project is to improve this enzyme, further by targeted mutagenesis.

## Related work, problems, or tasks in the literature
Enzyme engineering used to be a labor-intensive undertaking. With recent advancements in artificial intelligence, also this field has become more data driven, and faster paced. Structure prediction models, machine learning and reinforcement learning have allowed researchers to improve enzymes, and even create de novo enzymes with little cash or time investment (Khan and Khan, 2026; Middendorf and Ferruz, 2026). Online platforms for enzyme engineering are being hosted, for example: EnzymeMiner, a web server for automated screening and annotation of diverse family members that enables selection of hits for wet-lab experiments (Hon et al. 2020). Ideally this is coupled with a high throughput experimental platform where generated can directly be synthesized, expressed and tested (Landwehr *et al,* 2025). A step by step artificial intelligence-based workflow for enzyme optimization is described by Khan and Khan (2026).

## Explain the task to be solved
- Identify which parts of the enzyme are essential for its functioning (the catalytic triad, and other residues conserved within the atropinesterases).
- Identify which non-essential parts may contribute to a lower solubility and put these residues on a list of candidates for mutation into a more favorable residue. Generally hydrophobic residues on the protein surface reduce solubility, while hydrophilic residues improve solubility. 
- Feed the list of candidates to ESM generative AI to see in the nearby sequence context a mutation into which residue would be evolutionarily favored. 
- Filtering, scoring, and ranking, to obtain a list of variants with two point mutations.
- use generative AI (OpenFold2) to predict their structures.
- A good variant would have preserved the general structure of the target, especially for the residues in the catalytic triad, it would have better stability metrics, and lower number of hydrophobic surface exposure. Top candidates may then be synthesized and tested in the wet lab.

<img src="images/Model%20architecture.png" alt="Model architecture">

## Describe the dataset
1.	Amino acid sequences of the 6 identified atropinesterases `fasta/atropinesterases.fasta`
2.	A multiple sequence alignment of the 6 identified atropinesterases `fasta/atropinesterases_alignment.a3m`
3.	AlphaFold2 models of 2 of the 6 atropinesterases `pdb/AF-A0A2D9RK65-F1-model_v6.pdb` `pdb/AF-A0A4R9PVA8-F1-model_v6.pdb`
4.	The multiple sequence alignment files that were used to make these models (containing many other alpha beta hydrolases, mostly not atropinesterases) `fasta/AF-A0A2D9RK65-F1-msa_v6.a3m` `fasta/AF-A0A4R9PVA8-F1-msa_v6.a3m`
5.	The A tandoii atropinesterase multiple sequence alignment generated by moving to the top position (query) in two above mentioned a3m files `fasta/AF-A0A515BEI4-F1-msa_v6.a3m` the above mentioned (4) A0A2D9RK65 a3m file.
6.	An AlphaFold2 model of A. tandoii atropinesterase `pdb/A0A515BEI4_AlphaFold2_model_2_seed_000.pdb`, which I generated on (https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/AlphaFold2.ipynb), using the above mentioned (5) A tandoii atropinesterase sequence a3m file. 

## Preprocess data and explain the process
In the dataset, one could consider parts 2, 5, and 6 as already belonging to the data preprocessing, using parts 1, 4 of the raw data. The next preprocessing step is annotating the residues that make up the enzyme.

In cell 3 of the jpynb, the multiple sequence alignment of the 6 atropinesterases is loaded, and to identify conserved amino acids. In cell 4 conserved amino acids and also explicitly the amino acids that make up the catalytic triad of the target enzyme are assigned a locked status, meaning they are not to be considered for mutation.

In cells 7 and 8, the 3d structures of the proteins are loaded, and mapped to the sequence alignment. In cells 9 and 10, it is established that the structural models we use have a high per-residue local confidence, using the predicted local distance difference test (pLDDT), and that the three homologous models are folded likewise, by calculating the root mean square deviation (RMSD) between aligned residues.

The data is now aligned, mapped, labeled and annotated in a way that it is readily usable for the machine learning process.

## Explain your model, model architecture, parameters, methods, etc.
The isoelectric point and the enzyme’s charge state at typical experiment pH values were calculated in cell 5. Typically, if a protein has a near zero net charge, it will be more prone to aggregation, in which case charged residues could be targeted for mutation to achieve a different isoelectric point. In our case, the protein has good charge properties, with a net excess of around 10 electrons (the proteins would repel each other in solution, reducing the chance for aggregate formation).

In cell 6 the stickiness is evaluated. It is observed that all atropinesterases have a substantial fraction of hydrophobic residues, and some of these are clustered together within the primary structure. Hydrophobic regions tend to seek interaction with other hydrophobic regions, in order to avoid interaction with water. The result of this cell indicates that hydrophobic interactions may play an important role in the aggregate formation. Especially the bulky side chains from aromatic amino acids tryptophan and phenylalanine can contribute to a large hydrophobic surface. The aromatic residues are not necessarily overrepresented, at 10%.

In cells 11 and 12, the structural data is combined with hydrophobicity analysis to determine the fraction of hydrophobic residues on the surface, and the largest number of hydrophobic residues in patch with an 8 Å radius around one residue. 

In cell 13, residues that improve conformational stability are identified. A first requirement is for residues to have a high pLDDT value (predicted local distance difference test). pLDDT is a value (0-100) given by AlphaFold to each residue during folding to indicate local confidence. Well structured regions have a high pLDDT, while flexible or unstructured regions have low pLDDT (these regions are difficult to crystalize, so there is less data). In addition to pLDDT, residues with many neighbor contacts are considered as structurally stabilizing.
Cell 14, and 15 combine alignment with structure to identify structurally unstable positions in the target. These are good candidates for mutation. They are ranked according to a mutation priority score, which is combines low confidence and low packing scores. In cell 16, surface hydrophobicity is applied as the final filter, before obtaining the definitive list of mutable residues with their associated `mutation_priority_score`.
 
ESM mutation search (cell 17) is used for mutation proposal. The list of mutable residues is scanned in a *plausibility filter*. From a large database of protein sequences, the model has learned the statistical rules that allow it to assess the proposed mutations in the context of the local sequence of amino acids. I have excluded mutations to cysteine from being proposed, as these mutation could lead to two proteins forming covalent cystine bridges, which would increase aggregation probability. Each mutation will receive a ΔlogP score. If ΔlogP is close to 0, the proposed mutation is equally plausible as the wild type residue. The more negative the ΔlogP is, the more it would go against the evolutionary conventions, while a more positive ΔlogP means that the mutation would make the protein more aligned with common sequence patterns. 

ESM ΔlogP shows a normal distribution, skewed to positive ΔlogP, indicating that the initial filtering already prevents many unfavorable mutations from being considered:
<img src="images\ESM_dlogP_basecase.png" alt="ESM ΔlogP">

In cell 18, mutations with negative ΔlogP score are filtered out, and the mutations are classified by their chemical characteristics. Cell 19 combines the ESM `delta_logp` with the structure derived `mutation_priority_score`, using the weights defined in cell 1: `W_ESM` and `W_STRUCT`. This allows to rank mutations based on both metrics. In cell 20, for each position in the target, only the top three mutations are selected. Also mutations with a low final score are removed. 

Cell 21 uses the list with remaining mutations to make double mutation variants. To avoid destabilizing the local structure, the two mutations must be at least 5 residues apart from each other. The double mutation variants are sorted (descending) by the mean final score of the two individual single mutations. The top 20 variants with a mean score of at least 0.5 are then selected (cell 22). These variants are stored in a `.fasta` file (cell 23), and variant an `.a3m` file is generated, containing the alignment of the variant with every know close and distant homolog (cell 24). 

Cell 25 uploads the generated `.a3m` files of each variant to (https://health.api.nvidia.com/v1/biology/openfold/) for online structure prediction. As the files are around 7 MB each, there is a waiting time between each upload, to prevent overloading the server. For the folding of the different scenarios, there is a check to see if the structure for the same set of mutations has already been generated previously, so they can be copied with new metadata, and repeated structure prediction is avoided.

Cells 25 and 26 perform different metrics on the generated variant structures. Included are the distances between the residues in the catalytic triad, and the root mean square deviation (RMSD). The RMSD is used to measure the similarity of two structures. The distances between each residues Cα atomic coordinates after optimal rigid body superposition are combined into a single RMSD value that quantifies the overall structural deviation of the entire protein backbone relative to the reference structure:
<div style="background-color: white; display: inline-block; padding: 4px;">
  <img src="images\RMSD.svg" width="200" alt="RMSD formula">
</div>

(https://wikimedia.org/api/rest_v1/media/math/render/svg/bf0d0f19a819f1744ab3ef2f740cac54e69d6a23)

RMSD is measured between variant and target, and between the variants amongst themselves. With an RMSD cutoff, variant basins with close structural similarity can be established. These structural basins are visualized in cell 28.

In cells 29 and 30, the variants are scored based on a composite score encompassing numerous metrics. Aggregation prone proteins usually have hydrophobic surfaces, reduced compactness, and higher structural variation. For a high score, structures should have:
- Low nearest neighbor RMSD (structural consistency)
- High contact density and low radius of gyration (more compact)
- Low exposed hydrophobic residues (reduced aggregation tendency)
- Net charge close to the target's net charge (low charge deviation)
Finally in cell 31, Pareto front plots are generated, to show RMSD to target and the Exposed hydrophobic fraction, and potential trade-offs between these two objectives lead to each variant's final composite score.

## Experiment with your model. Change it, tune hyperparameters, etc. Explain your final model
It has to be taken into account that every .pdb file in this study, whether raw data, or generated in the pipeline, is ultimately derived from the same alignment, and there is no use of direct experimental evidence for any atropinesterase structure.
I have used several threshold and scoring methods in different scenarios, to evaluate their impact on which mutants would be selected in the top 20 for folding and further analysis (cell 0). 
- I tried out different values for `MIN_NEIGHBORS_BURIED` to change the likelihood for residues to get the `is_surface_residue status`. One with lower threshold leading to less residues being identified as surface residues, and one with a higher threshold, leading to more residues identified as being on the surface (number of surface residues in target: basecase 152, strict 83, tolerant 230).
-	I tried changing the weighting between my target structure, and the two Uniprot/AlphaFold2 structures (`SEQ_WEIGHTS`) to steer their influence on mutable residue selection, but as it turned out, between these highly similar structures, there is no difference in selectivity.
-	I varied `W_ESM` and `W_STRUCT`, to establish in what extent the ESM Δlog P score and the priority score based on structural metrics, influencing respectively which mutations are evolutionarily preferred, and which residues are preferably first mutated. In the scenario with a high `W_struct`, after filtering the single mutations, there were only 9 mutations selected for generating double mutation variants, but all their residues were within a narrow range (residue numbers 167-171), violating the rule that the two mutations must be at least five bases apart from each other, in order to prevent locally destabilizing the structure.

## Explain and visualize your results

Different scenarios (hyperparameter tunings) propose different combinations of double mutations. We can compare the proposed mutations for each scenario in a similarity heatmap.

<img src="analysis\figures\scenario_similarity_heatmap.png" alt="Similarity Heatmap, non-filtered">  

It directly becomes clear that scenarios 00, 03, 04, 05, and 07 al generated the same set of variants; the settings of the alternate scenarios did not alter the outcome compared to the base case. To prevent skewing the statistics, I will exclude the duplicate scenarios, so this would be the new similarity heatmap:

<img src="analysis\filtered\figures\scenario_similarity_heatmap.png" alt="Similarity Heatmap, filtered">  

Seven residues were dominating the top 20 in these four scenarios: 

<img src="analysis\filtered\figures\dominant_residues.png" alt="Dominant residues, filtered">

Still, different residues are preferred depending on the scenario:

<img src="analysis\filtered\figures\scenario_residue_heatmap.png" alt="Scenario residue heatmap, filtered">

N15P_Y157D was most often a top 20 contender. N15P appears 8 times in the overall top 10, with at least 2 scenarios having this mutation in its top 20.

<img src="analysis\filtered\figures\robust_variants.png" alt="Robust variants, filtered">

Different scenarios show distinct frequencies of residue use, and while some variants were present in multiple scenarios, in the four scenarios, meaning four top 20's, there should be 80 variants in total. The little overlap of variants between scenarios means that each scenario illustrated here resulted in many new top 20 variants.

---
For the top 20 variants, structures were generated, using OpenFold2 on NVIDIA NIM (https://build.nvidia.com/openfold/openfold2). Below are the metrics of the base case structures. The catalytic triad geometry appears well preserved in every variant. The variants are all structurally closer to other variants, than they are to the target structure, and with a nearest variant RMSD cutof of 0.8, the variants of the base case split into two structural basins.

| Variant ID               | Coverage | Triad OK | d_Ser–His | d_His–Asp | d_Ser–Asp | Target RMSD | Nearest Variant RMSD | PASS | Basin ID |
|--------------------------|----------|----------|-----------|-----------|-----------|-------------|----------------------|------|----------|
| TARGET                   | 1.0      | True     | 10.8276   | 4.4895    | 7.6868    | NaN         | NaN                  | True | NaN      |
| VAR_05_E167L_G267L       | 1.0      | True     | 10.7854   | 4.6721    | 7.6696    | 2.1151      | 0.0942               | True | BASIN_01 |
| VAR_14_E167V_G267L       | 1.0      | True     | 10.7580   | 4.6696    | 7.6712    | 2.1198      | 0.0942               | True | BASIN_01 |
| VAR_06_E167I_G267L       | 1.0      | True     | 10.7869   | 4.6679    | 7.6665    | 2.0870      | 0.1254               | True | BASIN_01 |
| VAR_03_E167L_G267F       | 1.0      | True     | 10.8558   | 4.6907    | 7.7190    | 2.3096      | 0.1570               | True | BASIN_01 |
| VAR_04_E167I_G267F       | 1.0      | True     | 10.8722   | 4.6939    | 7.7287    | 2.2521      | 0.1570               | True | BASIN_01 |
| VAR_02_E167I_G267V       | 1.0      | True     | 10.7873   | 4.5730    | 7.6055    | 1.7410      | 0.1901               | True | BASIN_01 |
| VAR_07_E167V_G267V       | 1.0      | True     | 10.7448   | 4.5524    | 7.5865    | 1.8660      | 0.1901               | True | BASIN_01 |
| VAR_01_E167L_G267V       | 1.0      | True     | 10.7948   | 4.5858    | 7.6246    | 2.0102      | 0.2494               | True | BASIN_01 |
| VAR_10_E167V_G267F       | 1.0      | True     | 10.8407   | 4.6759    | 7.7083    | 2.4172      | 0.2503               | True | BASIN_01 |
| VAR_08_A171F_G267V       | 1.0      | True     | 10.7637   | 4.5810    | 7.5893    | 1.8343      | 0.2716               | True | BASIN_01 |
| VAR_12_A171F_G267F       | 1.0      | True     | 10.8705   | 4.6823    | 7.6966    | 1.8768      | 0.2953               | True | BASIN_01 |
| VAR_15_A171F_G267L       | 1.0      | True     | 10.7886   | 4.6745    | 7.6597    | 2.1001      | 0.2969               | True | BASIN_01 |
| VAR_16_A171L_G267V       | 1.0      | True     | 10.7536   | 4.5565    | 7.7438    | 1.8740      | 0.3297               | True | BASIN_01 |
| VAR_19_A171L_G267F       | 1.0      | True     | 10.8026   | 4.6377    | 7.8166    | 2.0330      | 0.3297               | True | BASIN_01 |
| VAR_17_Y157D_E167I       | 1.0      | True     | 10.6990   | 4.5083    | 7.5489    | 2.5041      | 0.4252               | True | BASIN_01 |
| VAR_13_Y157D_E167L       | 1.0      | True     | 10.6945   | 4.4864    | 7.6907    | 1.9291      | 0.4643               | True | BASIN_01 |
| VAR_18_R168K_G267V       | 1.0      | True     | 10.7514   | 4.5294    | 7.7399    | 1.8848      | 0.5967               | True | BASIN_01 |
| VAR_09_N15P_E167L        | 1.0      | True     | 10.7109   | 4.5215    | 7.5072    | 0.6217      | 0.0819               | True | BASIN_02 |
| VAR_11_N15P_E167I        | 1.0      | True     | 10.7318   | 4.5263    | 7.5115    | 0.6357      | 0.0819               | True | BASIN_02 |
| VAR_20_N15P_E167V        | 1.0      | True     | 10.6898   | 4.4923    | 7.5226    | 0.6150      | 0.0988               | True | BASIN_02 |

The RMSD between variants, and their basins are also visualized in the figures below, clearly showing how variants 9, 11, and 20 are in a distinct fold basin:  
<img src="images\Pairwise_RMSD_basacase.png" alt="Pairwise RMSD base case"><img src="images\Dendrogram_basecase.png" alt="Dendogram base case">

In the table below, the main metrics used for the final composite score are shown.
| Variant ID               | Target RMSD | Nearest Variant RMSD | Exposed Hydrophobic Fraction | Largest Hydrophobic Patch | Radius of Gyration | Composite Score | Global Rank |
|--------------------------|-------------|----------------------|------------------------------|---------------------------|--------------------|-----------------|-------------|
| VAR_20_N15P_E167V        | 0.615       | 0.099                | 0.285                        | 17                        | 16.787             | 0.842           | 1           |
| VAR_09_N15P_E167L        | 0.622       | 0.082                | 0.289                        | 17                        | 16.788             | 0.822           | 2           |
| VAR_14_E167V_G267L       | 2.120       | 0.094                | 0.288                        | 15                        | 16.823             | 0.682           | 3           |
| VAR_02_E167I_G267V       | 1.741       | 0.190                | 0.293                        | 15                        | 16.803             | 0.663           | 4           |
| VAR_07_E167V_G267V       | 1.866       | 0.190                | 0.293                        | 15                        | 16.800             | 0.647           | 5           |
| VAR_06_E167I_G267L       | 2.087       | 0.125                | 0.288                        | 15                        | 16.835             | 0.627           | 6           |
| VAR_11_N15P_E167I        | 0.636       | 0.082                | 0.296                        | 24                        | 16.778             | 0.592           | 7           |
| VAR_05_E167L_G267L       | 2.115       | 0.094                | 0.296                        | 15                        | 16.843             | 0.577           | 8           |
| VAR_08_A171F_G267V       | 1.834       | 0.272                | 0.291                        | 16                        | 16.805             | 0.559           | 9           |
| VAR_15_A171F_G267L       | 2.100       | 0.297                | 0.286                        | 15                        | 16.833             | 0.529           | 10          |
| VAR_04_E167I_G267F       | 2.252       | 0.157                | 0.297                        | 16                        | 16.828             | 0.528           | 11          |
| VAR_01_E167L_G267V       | 2.010       | 0.249                | 0.300                        | 15                        | 16.811             | 0.526           | 12          |
| VAR_12_A171F_G267F       | 1.877       | 0.295                | 0.287                        | 15                        | 16.832             | 0.525           | 13          |
| VAR_03_E167L_G267F       | 2.310       | 0.157                | 0.306                        | 16                        | 16.820             | 0.509           | 14          |
| VAR_19_A171L_G267F       | 2.033       | 0.330                | 0.286                        | 16                        | 16.859             | 0.442           | 15          |
| VAR_10_E167V_G267F       | 2.417       | 0.250                | 0.297                        | 17                        | 16.830             | 0.410           | 16          |
| VAR_13_Y157D_E167L       | 1.929       | 0.464                | 0.289                        | 16                        | 16.832             | 0.390           | 17          |
| VAR_17_Y157D_E167I       | 2.504       | 0.425                | 0.297                        | 17                        | 16.816             | 0.313           | 18          |
| VAR_16_A171L_G267V       | 1.874       | 0.330                | 0.299                        | 17                        | 16.849             | 0.292           | 19          |
| VAR_18_R168K_G267V       | 1.885       | 0.597                | 0.290                        | 24                        | 16.858             | 0.129           | 20          |

The two highest ranked variants are both from basin 2, and the third variant (VAR_11) in basin 2 is also still ranked quite high, on the 7th position. A defining mutation in this basin is the N15P mutation. Already during the comparison of the different residues and mutations for the different scenarios, that residue 15 and the mutation N15P were highly preferred, and this is now also confirmed by the composite metrics of the base case. From the table, we can see that all basin 2 variants have a low RMSD to target, this is even more evident in the Pareto front and landscape plots:

<img src="images\2D_Pareto_front_basecase.png" alt="2D Pareto base case">
<img src="images\3D_Pareto_landscape_basecase.png" alt="3D Pareto base case">

All the basin 2 variants are situated at the left part of the plot, with low RMSD to target. 

The Pareto optimal variants per scenario (be aware that strict_surface scenarios inherently use a smaller subset of residues to calculate the exposed_hydrophobic_fraction and therefore a direct comparison of composite scores is not possible). Only the N15P_C241L variant was a pareto optimal variant in multiple (two) scenarios.

| Scenario                         | Variant ID               | Target RMSD |
|----------------------------------|--------------------------|-------------|
| 00_basecase                      | VAR_20_N15P_E167V        | 0.62        |
| 01_high_W_esm                    | VAR_20_N15P_C241L *      | 0.32        |
| 01_high_W_esm                    | VAR_18_N15P_H212E        | 0.36        |
| 01_high_W_esm                    | VAR_05_Y102L_G267V       | 1.94        |
| 01_high_W_esm                    | VAR_14_Y102L_G267L       | 2.11        |
| 01_high_W_esm                    | VAR_17_N15G_G267F        | 2.13        |
| 01_high_W_esm                    | VAR_03_N15P_G267L        | 0.82        |
| 06_strict_surface                | VAR_05_N15P_A171Y        | 0.61        |
| 06_strict_surface                | VAR_03_N15P_A171L        | 0.64        |
| 06_strict_surface                | VAR_07_N15P_Y157D        | 0.57        |
| 08_high_W_esm_strict_surface     | VAR_04_N15P_C241L *      | 0.32        |
| 08_high_W_esm_strict_surface     | VAR_02_N15P_C241K        | 0.32        |

Again N15P domination is observed. If I would rationalize the N15P mutation, it comes to mind that residue 15 is close to the N-terminus. This residue it at the boundary between the disordered N-terminal tail, and the first secondary structures in the protein. Mutation to proline makes the backbone more rigid. As this mutation is proposed through ESM scan, some rigidity at this part of the protein could be favorable, both for the stability of the structure, and for avoiding unfolding at the N-terminus.

This study demonstrates a fully computational pipeline, that uses generative AI to identify atropinesterase variants with improved solubility, while preserving the overall structure, and the structure of the catalytic site. Sequence and strucute attributes were combined and resulted in robuts indentification of the N15P mutation.

## List the lessons you learned, and challenges faced during the project. Point out further work or ideas
There are multiple aspects that contribute to solubility of enzymes, and thereforethere are also multiple design objectives. These objectives may sometimes compete, so it is important to find the correct balance. The Pareto front analysis helped to visualize the impact of two main objectives, structural integrity and low hydrophobic surface exposure, on the final composite score.

The main difficulty was to get the folding running, an essential part of this project. I had tried different folding methods, the first few wouldn’t work on my hardware, or even on modal. For doing everything locally, the problem was that the latest ESMFold and OpenFold packages required a CUDA version not supporting my GPU. On Modal, I needed a custom package that was not pip installable, and I was not allowed to install it from a GitHub repository either.

When I finally settled on NVIDIA NIM, I originally used it with my query, and just one template sequence, resulting in RMSD between the variant structures and target structure, to be in the order of 20. The RMSD between the different variant was smaller (6-10), but still substantial. I explored the option of running a prediction of every variant sequence on the online AlphaFold2 notebook (https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/AlphaFold2.ipynb), when I noticed that the AlphaFold2 structures for homologs A0A2D9RK65 (https://alphafold.ebi.ac.uk/entry/AF-A0A2D9RK65-F1) and A0A4R9PVA8 (https://alphafold.ebi.ac.uk/entry/AF-A0A4R9PVA8-F1) came with a large multiple sequence alignments. Using these alignment files, but with my target or variant sequences as the query greatly improved RMSD’s of the structures generated by the NVIDIA NIM method.

One further work implied by this study, is to assess the solubility and selectivity and activity of the top variants in the wet-lab. Apart from this, computationally, it should be possible to use a docking model to see how the substrate atropine fits in the active site of the protein. Given the low RMSD values for the different variants, the *in-silico* substrate docking should be successful. Using large alignment files, and structural alignment, it should also be possible to identify more atropinesterases in current available databases. 

It would also be interesting to see if less soluble and less stable variants (according to composite score) would be generated when aiming to mutate the lowest priority residues (I would not touch the locked residues), and selecting the most negative ΔlogP scores. If the model is correct for predicting solubility, this strategy should result in obtaining the variants most prone to aggregation.

Finally, this work can also be expanded to other enzymes. The challenge of atropinesterases, is the scarcity of available data (genomic sequences, proteomic data, biochemical evaluation, and structural data). With more extensively studied enzymes, there would be a richer dataset, so the *in-silico* work wold be more informed, and moreover there might even already be experimental data for some of the variants that would be selected as top candidates by the *in-silico* pipeline.

## Instructions for running the code
```python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-genai.txt
code .
```
go to https://build.nvidia.com/openfold/openfold2  
register and get an API key  
paste the key into .env  
`pip install python-dotenv`

**in Python:**
```import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("API_KEY")
print(api_key) # to test
```

## Generative AI disclosure

I have used Generative AI to help with creation of figures, the ESM mutation search, the API key and session management of NVIDIA NIM, for refactoring of code into functions to be re-used across the pipeline, and for debugging.

## References

**Bartholomew, B.A., Smith, M.J., Trudgill, P.W. and Hopper, D.J. (1996)**
Atropine metabolism by *Pseudomonas* sp. strain AT3: evidence for nortropine as an intermediate in tropine breakdown and reactions leading to succinate. *Applied and Environmental Microbiology*, **62**(9), pp. 3245–3250.

**Brust, J.C.M. (2004)**
Anticholinergics. In: J.C.M. Brust (ed.) *Neurological Aspects of Substance Abuse*. 2nd edn. Philadelphia: Butterworth-Heinemann, pp. 309–315.
[https://doi.org/10.1016/B978-0-7506-7313-6.50015-5](https://doi.org/10.1016/B978-0-7506-7313-6.50015-5)

**Hon, J., Borko, S., Stourac, J., Prokop, Z., Zendulka, J., Bednar, D., Martinek, T. and Damborsky, J. (2020)**
EnzymeMiner: automated mining of soluble enzymes with diverse structures, catalytic properties and stabilities. *Nucleic Acids Research*, **48**(W1), pp. W104–W109.
[https://doi.org/10.1093/nar/gkaa372](https://doi.org/10.1093/nar/gkaa372)

**Khan, M.F. and Khan, M.T. (2026)**
AI-driven enzyme engineering: emerging models and next-generation biotechnological applications. *Molecules*, **31**(1), article 45.
[https://doi.org/10.3390/molecules31010045](https://doi.org/10.3390/molecules31010045)

**Landwehr, G.M., Bogart, J.W., Magalhaes, C., Hammarlund, E.G., Karim, A.S. and Jewett, M.C. (2025)**
Accelerated enzyme engineering by machine-learning guided cell-free expression. *Nature Communications*, **16**(1), article 865.
[https://doi.org/10.1038/s41467-024-55399-0](https://doi.org/10.1038/s41467-024-55399-0)

**Middendorf, L. and Ferruz, N. (2026)**
Generative AI for enzyme design and biocatalysis. *arXiv*. Available at: [https://arxiv.org/abs/2602.03779](https://arxiv.org/abs/2602.03779) (Accessed: 16 February 2026).

**Rörsch, A., Berends, F., Bartlema, H.C. and Stevens, W.F. (1971)**
The isolation and properties of *Pseudomonas* strains growing on atropine and producing atropinesterase. *Proceedings of the Koninklijke Nederlandse Akademie van Wetenschappen. Series C: Biological and Medical Sciences*, **74**(2), pp. 132–147.


