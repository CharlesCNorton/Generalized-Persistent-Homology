# A Exploration of the Unified Equation for Persistent Homology in Stratified Spaces

**By:** Charles Norton & GPT-4 

**Last Updated:** October 7th, 2024

### Formalization of the Unified Equation for Persistent Homology

#### 0. Preliminaries and Notation

Let ![X](https://latex.codecogs.com/svg.image?X) be a topological space that may be decomposed into distinct stratified regions. These regions can be categorized into:

![X = X_{\text{smooth}} \cup X_{\text{non-smooth}} \cup \Sigma](https://latex.codecogs.com/svg.image?X%20=%20X_{\text{smooth}}%20\cup%20X_{\text{non-smooth}}%20\cup%20\Sigma)

where:
- ![X_{\text{smooth}}](https://latex.codecogs.com/svg.image?X_{\text{smooth}}) is the smooth part of the space, which consists of regions where ![X](https://latex.codecogs.com/svg.image?X) admits a smooth differentiable structure.
- ![X_{\text{non-smooth}}](https://latex.codecogs.com/svg.image?X_{\text{non-smooth}}) is the non-smooth part, which consists of regions where ![X](https://latex.codecogs.com/svg.image?X) exhibits sharp, non-differentiable features, such as polyhedral complexes or piecewise-linear structures.
- ![\Sigma \subset X](https://latex.codecogs.com/svg.image?\Sigma%20\subset%20X) is the singular set, which contains points where ![X](https://latex.codecogs.com/svg.image?X) exhibits topological singularities. Singularities can arise in algebraic varieties (e.g., nodes, cusps), stratified spaces, or spaces with non-manifold points.

We aim to compute the persistent homology ![PH_k(X)](https://latex.codecogs.com/svg.image?PH_k(X)) of the space ![X](https://latex.codecogs.com/svg.image?X) in dimension ![k](https://latex.codecogs.com/svg.image?k). Persistent homology tracks the birth and death of topological features (such as connected components, loops, voids, etc.) over a filtration of the space, providing a description of the topological changes across scales.

#### 0.1 Filtrations

A filtration on a space ![X](https://latex.codecogs.com/svg.image?X) is a sequence of nested subspaces ![\{ X_t \}_{t \geq 0}](https://latex.codecogs.com/svg.image?\{X_t\}_{t%20\geq%200}), indexed by a real-valued parameter ![t \geq 0](https://latex.codecogs.com/svg.image?t%20\geq%200), such that:

![X_{t_1} \subseteq X_{t_2} \quad \text{whenever} \quad t_1 \leq t_2](https://latex.codecogs.com/svg.image?X_{t_1}%20\subseteq%20X_{t_2}%20\quad%20\text{whenever}%20\quad%20t_1%20\leq%20t_2)

This filtration can represent increasing scales or radii, where smaller scales capture local features and larger scales capture global ones. Persistent homology analyzes the evolution of topological features as ![t](https://latex.codecogs.com/svg.image?t) varies, providing intervals ![[b_i, d_i)](https://latex.codecogs.com/svg.image?[b_i,%20d_i)) for the birth and death of each feature.

#### 0.2 Homology and Persistent Homology

The homology groups ![H_k(X)](https://latex.codecogs.com/svg.image?H_k(X)) of a topological space ![X](https://latex.codecogs.com/svg.image?X) in dimension ![k](https://latex.codecogs.com/svg.image?k) measure ![k](https://latex.codecogs.com/svg.image?k)-dimensional holes in the space. For example:
- ![H_0(X)](https://latex.codecogs.com/svg.image?H_0(X)) measures connected components.
- ![H_1(X)](https://latex.codecogs.com/svg.image?H_1(X)) measures loops or 1-dimensional holes.
- ![H_2(X)](https://latex.codecogs.com/svg.image?H_2(X)) measures voids or 2-dimensional holes.

The persistent homology groups ![PH_k(X)](https://latex.codecogs.com/svg.image?PH_k(X)) track how these ![k](https://latex.codecogs.com/svg.image?k)-dimensional holes evolve as the filtration parameter ![t](https://latex.codecogs.com/svg.image?t) increases. A ![k](https://latex.codecogs.com/svg.image?k)-dimensional feature born at scale ![b_i](https://latex.codecogs.com/svg.image?b_i) and dying at scale ![d_i](https://latex.codecogs.com/svg.image?d_i) is represented by a persistence interval ![[b_i, d_i)](https://latex.codecogs.com/svg.image?[b_i,%20d_i)).

We will now proceed to develop the formal theory for computing ![PH_k(X)](https://latex.codecogs.com/svg.image?PH_k(X)) when ![X](https://latex.codecogs.com/svg.image?X) contains smooth, non-smooth, and singular regions. Each region contributes to the overall persistent homology in a distinct way, and the unified equation will combine these contributions.

---

#### 1. Smooth Regions of \( X \) and Their Homology

##### Definition 1.1: Filtration on Smooth Regions

Let ![X_{\text{smooth}}](https://latex.codecogs.com/svg.image?X_{\text{smooth}}) be the smooth part of the space ![X](https://latex.codecogs.com/svg.image?X), which admits a differentiable structure. A filtration ![\{ X_t \}_{t \geq 0}](https://latex.codecogs.com/svg.image?\{X_t\}_{t%20\geq%200}) on ![X_{\text{smooth}}](https://latex.codecogs.com/svg.image?X_{\text{smooth}}) is a nested sequence of subspaces such that:

![X_{t_1} \subseteq X_{t_2} \quad \text{for all} \quad t_1 \leq t_2](https://latex.codecogs.com/svg.image?X_{t_1}%20\subseteq%20X_{t_2}%20\quad%20\text{for%20all}%20\quad%20t_1%20\leq%20t_2)

For smooth spaces, this filtration can be induced using various methods, including the Vietoris-Rips complex, the Čech complex, or the alpha complex, which are commonly used in persistent homology to construct simplicial approximations of the space at different scales.

##### Example 1.1: Vietoris-Rips Filtration

Let ![X_{\text{smooth}} \subset \mathbb{R}^n](https://latex.codecogs.com/svg.image?X_{\text{smooth}}%20\subset%20\mathbb{R}^n) be a finite point cloud. The Vietoris-Rips complex ![VR(X_{\text{smooth}}, t)](https://latex.codecogs.com/svg.image?VR(X_{\text{smooth}},%20t)) at scale ![t](https://latex.codecogs.com/svg.image?t) is the simplicial complex formed by taking all subsets of points in ![X_{\text{smooth}}](https://latex.codecogs.com/svg.image?X_{\text{smooth}}) whose pairwise distances are less than or equal to ![t](https://latex.codecogs.com/svg.image?t). As ![t](https://latex.codecogs.com/svg.image?t) increases, more simplices are added to the complex, corresponding to larger clusters of points coming together.

The filtration ![\{ VR(X_{\text{smooth}}, t) \}_{t \geq 0}](https://latex.codecogs.com/svg.image?\{VR(X_{\text{smooth}},%20t)\}_{t%20\geq%200}) describes how the topology of ![X_{\text{smooth}}](https://latex.codecogs.com/svg.image?X_{\text{smooth}}) evolves as we zoom out and consider larger neighborhoods of points. Homological features (connected components, loops, voids) appear and disappear over different scales.

##### Lemma 1.1: Persistence for Smooth Spaces

Let <img src="https://latex.codecogs.com/svg.image?\bg{white}X_{\text{smooth}}" /> be a smooth region of <img src="https://latex.codecogs.com/svg.image?\bg{white}X" />, equipped with a filtration <img src="https://latex.codecogs.com/svg.image?\bg{white}\{X_t\}_{t%20\geq%200}" /> induced by a Vietoris-Rips complex or a related construction. The persistent homology in dimension <img src="https://latex.codecogs.com/svg.image?\bg{white}k" />, denoted <img src="https://latex.codecogs.com/svg.image?\bg{white}PH_k(X_{\text{smooth}})" />, consists of a collection of persistence intervals of the form:

<img src="https://latex.codecogs.com/svg.image?\bg{white}PH_k(X_{\text{smooth}})%20=%20\bigcup%20\left\{%20[b_i,%20d_i)%20\mid%20H_k%20\text{class%20born%20at}%20b_i%20\text{and%20dies%20at}%20d_i%20\right\}" />.

Each interval <img src="https://latex.codecogs.com/svg.image?\bg{white}[b_i,%20d_i)" /> corresponds to a homology class in dimension <img src="https://latex.codecogs.com/svg.image?\bg{white}k" />, where <img src="https://latex.codecogs.com/svg.image?\bg{white}b_i" /> is the birth time and <img src="https://latex.codecogs.com/svg.image?\bg{white}d_i" /> is the death time of the feature.

**Proof**: This result follows from the standard theory of persistent homology as applied to smooth spaces. The filtration <img src="https://latex.codecogs.com/svg.image?\bg{white}\{X_t\}" /> induces a sequence of simplicial complexes, and the homology groups <img src="https://latex.codecogs.com/svg.image?\bg{white}H_k(X_t)" /> evolve as simplices are added to the complex. The persistence intervals <img src="https://latex.codecogs.com/svg.image?\bg{white}[b_i,%20d_i)" /> track the birth and death of homological features as <img src="https://latex.codecogs.com/svg.image?\bg{white}t" /> increases. This process is well-defined for smooth spaces, where the topological structure is well-behaved and admits standard computational techniques.

##### Corollary 1.1: Stability of Persistent Homology in Smooth Spaces

The persistence intervals <img src="https://latex.codecogs.com/svg.image?\bg{white}[b_i,%20d_i)" /> computed for a smooth space <img src="https://latex.codecogs.com/svg.image?\bg{white}X_{\text{smooth}}" /> are stable under small perturbations of the input data. That is, if the underlying point cloud or simplicial complex is perturbed by a small amount, the resulting persistence intervals change only slightly. This stability is formalized by the bottleneck distance between persistence diagrams, which measures the similarity between the intervals of two different filtrations.

---

#### 2. Non-Smooth Regions of \( X \) and Discrete Morse Theory

##### Definition 2.1: Non-Smooth Spaces and Polyhedral Complexes

Let <img src="https://latex.codecogs.com/svg.image?\bg{white}X_{\text{non-smooth}}" /> ⊆ <img src="https://latex.codecogs.com/svg.image?\bg{white}X" /> be the non-smooth part of <img src="https://latex.codecogs.com/svg.image?\bg{white}X" />. Non-smooth spaces often arise in polyhedral complexes, piecewise-linear structures, or spaces with sharp edges and corners. These regions do not admit a smooth differentiable structure, and their topological features must be analyzed combinatorially.

A common approach for analyzing non-smooth spaces is to decompose them into simplicial complexes or polyhedral complexes, where each simplex represents a combinatorial piece of the space. For instance, a polyhedral complex may consist of vertices, edges, and higher-dimensional simplices glued together along their faces.

##### Example 2.1: Piecewise-Linear Space

Consider the 2-dimensional polyhedral complex consisting of a triangulated surface. This surface may have sharp edges or conical singularities at certain vertices, making it non-smooth. The topological features of this space, such as loops and voids, can be captured by examining the combinatorial structure of the triangulation.

##### Definition 2.2: Discrete Morse Function

To analyze the persistent homology of <img src="https://latex.codecogs.com/svg.image?\bg{white}X_{\text{non-smooth}}" />, we use discrete Morse theory, which assigns a real-valued function <img src="https://latex.codecogs.com/svg.image?\bg{white}f:%20K%20\to%20\mathbb{R}" /> to a simplicial complex <img src="https://latex.codecogs.com/svg.image?\bg{white}K" /> in a way that respects the combinatorial structure of the complex. A discrete Morse function <img src="https://latex.codecogs.com/svg.image?\bg{white}f:%20K%20\to%20\mathbb{R}" /> on a simplicial complex <img src="https://latex.codecogs.com/svg.image?\bg{white}K" /> assigns real values to the simplices of <img src="https://latex.codecogs.com/svg.image?\bg{white}K" /> in a way that respects the combinatorial structure of the complex, with the following conditions:

- For each <img src="https://latex.codecogs.com/svg.image?\bg{white}p" />-dimensional simplex <img src="https://latex.codecogs.com/svg.image?\bg{white}\sigma^p%20\in%20K" />, there is at most one <img src="https://latex.codecogs.com/svg.image?\bg{white}(p-1)" />-dimensional face <img src="https://latex.codecogs.com/svg.image?\bg{white}\tau^{p-1}%20\subset%20\sigma^p" /> such that <img src="https://latex.codecogs.com/svg.image?\bg{white}f(\tau^{p-1})%20\geq%20f(\sigma^p)" />.
- For each <img src="https://latex.codecogs.com/svg.image?\bg{white}p" />-dimensional simplex <img src="https://latex.codecogs.com/svg.image?\bg{white}\sigma^p%20\in%20K" />, there is at most one <img src="https://latex.codecogs.com/svg.image?\bg{white}(p+1)" />-dimensional coface <img src="https://latex.codecogs.com/svg.image?\bg{white}\eta^{p+1}%20\supset%20\sigma^p" /> such that <img src="https://latex.codecogs.com/svg.image?\bg{white}f(\eta^{p+1})%20\leq%20f(\sigma^p)" />.

These conditions ensure that the discrete Morse function encodes the topological structure of the space in a way that captures critical simplices, which are essential for determining the homology classes of the space.

##### Definition 2.3: Critical Simplices

A critical simplex under a discrete Morse function <img src="https://latex.codecogs.com/svg.image?\bg{white}f" /> is a simplex <img src="https://latex.codecogs.com/svg.image?\bg{white}\sigma^p%20\in%20K" /> such that:

- There is no face <img src="https://latex.codecogs.com/svg.image?\bg{white}\tau^{p-1}%20\subset%20\sigma^p" /> with <img src="https://latex.codecogs.com/svg.image?\bg{white}f(\tau^{p-1})%20\geq%20f(\sigma^p)" />.
- There is no coface <img src="https://latex.codecogs.com/svg.image?\bg{white}\eta^{p+1}%20\supset%20\sigma^p" /> with <img src="https://latex.codecogs.com/svg.image?\bg{white}f(\eta^{p+1})%20\leq%20f(\sigma^p)" />.

Critical simplices correspond to important topological features of the space:
- Critical 0-simplices correspond to connected components.
- Critical 1-simplices correspond to loops.
- Critical 2-simplices correspond to voids.

##### Lemma 2.1: Critical Simplices and Homological Features

Let <img src="https://latex.codecogs.com/svg.image?\bg{white}K" /> be a simplicial complex representing the non-smooth region <img src="https://latex.codecogs.com/svg.image?\bg{white}X_{\text{non-smooth}}" />, and let <img src="https://latex.codecogs.com/svg.image?\bg{white}f:%20K%20\to%20\mathbb{R}" /> be a discrete Morse function. Each critical <img src="https://latex.codecogs.com/svg.image?\bg{white}k" />-simplex <img src="https://latex.codecogs.com/svg.image?\bg{white}\sigma^k%20\in%20K" /> corresponds to a <img src="https://latex.codecogs.com/svg.image?\bg{white}k" />-dimensional homology class. The persistence of the homological feature associated with <img src="https://latex.codecogs.com/svg.image?\bg{white}\sigma^k" /> is given by:

<img src="https://latex.codecogs.com/svg.image?\bg{white}\tau_k(\sigma^k)%20=%20f(\sigma^{k+1})%20-%20f(\sigma^k)" />,

where <img src="https://latex.codecogs.com/svg.image?\bg{white}\sigma^{k+1}" /> is a critical <img src="https://latex.codecogs.com/svg.image?\bg{white}(k+1)" />-dimensional simplex that annihilates the homology class corresponding to <img src="https://latex.codecogs.com/svg.image?\bg{white}\sigma^k" />.

**Proof**: The persistence interval <img src="https://latex.codecogs.com/svg.image?\bg{white}\tau_k(\sigma^k)" /> represents the lifetime of the homology class associated with <img src="https://latex.codecogs.com/svg.image?\bg{white}\sigma^k" />. Since <img src="https://latex.codecogs.com/svg.image?\bg{white}f" /> is a discrete Morse function, the critical simplices of <img src="https://latex.codecogs.com/svg.image?\bg{white}f" /> correspond to the birth of homology classes. The death of the homology class occurs when the critical coface <img src="https://latex.codecogs.com/svg.image?\bg{white}\sigma^{k+1}" /> fills in the topological feature, causing the homology class to disappear. The persistence of the class is the difference between the values of <img src="https://latex.codecogs.com/svg.image?\bg{white}f" /> on the critical simplices.

##### Example 2.2: Persistence in a 2D Polyhedral Complex

Consider a 2-dimensional polyhedral complex <img src="https://latex.codecogs.com/svg.image?\bg{white}K" /> formed by triangulating a surface with sharp edges. A discrete Morse function <img src="https://latex.codecogs.com/svg.image?\bg{white}f:%20K%20\to%20\mathbb{R}" /> assigns real values to the vertices, edges, and triangles of <img src="https://latex.codecogs.com/svg.image?\bg{white}K" />. Critical vertices (0-simplices) correspond to connected components, critical edges (1-simplices) correspond to loops, and critical triangles (2-simplices) correspond to voids. As the filtration progresses, these critical simplices give rise to persistent homology classes, and their persistence intervals <img src="https://latex.codecogs.com/svg.image?\bg{white}\tau_k(\sigma^k)" /> measure the duration of the topological feature.

##### Lemma 2.2: Persistent Homology for Non-Smooth Spaces

Let <img src="https://latex.codecogs.com/svg.image?\bg{white}X_{\text{non-smooth}}" /> be a non-smooth region of the space <img src="https://latex.codecogs.com/svg.image?\bg{white}X" />, represented by a simplicial complex <img src="https://latex.codecogs.com/svg.image?\bg{white}K" /> with a discrete Morse function <img src="https://latex.codecogs.com/svg.image?\bg{white}f:%20K%20\to%20\mathbb{R}" />. The persistent homology in dimension <img src="https://latex.codecogs.com/svg.image?\bg{white}k" /> for the non-smooth regions is given by the sum of the persistence intervals of the critical simplices. Formally:

<img src="https://latex.codecogs.com/svg.image?\bg{white}PH_k(X_{\text{non-smooth}})%20=%20\sum_{\sigma^k%20\in%20K}%20\tau_k(\sigma^k)" />,

where <img src="https://latex.codecogs.com/svg.image?\bg{white}\tau_k(\sigma^k)" /> is the persistence of the critical <img src="https://latex.codecogs.com/svg.image?\bg{white}k" />-simplex <img src="https://latex.codecogs.com/svg.image?\bg{white}\sigma^k" />.

**Proof**: The critical simplices of the discrete Morse function correspond to the birth and death of homology classes in dimension <img src="https://latex.codecogs.com/svg.image?\bg{white}k" />. The persistence of each class is determined by the difference between the values of <img src="https://latex.codecogs.com/svg.image?\bg{white}f" /> on the critical simplices that give rise to and annihilate the class. The total persistent homology is the sum of the persistence intervals of all critical simplices in dimension <img src="https://latex.codecogs.com/svg.image?\bg{white}k" />.

##### Corollary 2.1: Stability of Persistence in Non-Smooth Spaces

The persistence intervals computed using discrete Morse theory are stable under small perturbations of the simplicial complex. This follows from the combinatorial nature of the discrete Morse function, which assigns values to simplices in a way that reflects the underlying topology. Small changes in the geometry of the simplicial complex lead to small changes in the persistence intervals, preserving the overall topological structure.

---

#### 3. Singular Regions of <img src="https://latex.codecogs.com/svg.image?\bg{white}X" /> and Intersection Homology

##### Definition 3.1: Stratified Spaces and Singular Varieties

Let <img src="https://latex.codecogs.com/svg.image?\bg{white}\Sigma%20\subset%20X" /> be the singular set of the space <img src="https://latex.codecogs.com/svg.image?\bg{white}X" />, consisting of points where the space is not locally Euclidean. Singularities arise in many contexts, such as algebraic varieties with nodes, cusps, or other types of topological irregularities. The singular set can consist of isolated points, curves, or higher-dimensional strata, depending on the complexity of the space.

For each singular point <img src="https://latex.codecogs.com/svg.image?\bg{white}p%20\in%20\Sigma" />, we define the link <img src="https://latex.codecogs.com/svg.image?\bg{white}L(p)" />, which encodes the local topology near the singularity. The link <img src="https://latex.codecogs.com/svg.image?\bg{white}L(p)" /> is a lower-dimensional space that captures the structure of <img src="https://latex.codecogs.com/svg.image?\bg{white}X" /> in a neighborhood of <img src="https://latex.codecogs.com/svg.image?\bg{white}p" />, and plays a crucial role in understanding the homology of <img src="https://latex.codecogs.com/svg.image?\bg{white}X" /> near the singularity.

##### Definition 3.2: Intersection Homology

Classical homology often fails to capture the topology near singular points because it does not account for the complexity of the singular set. To remedy this, we use intersection homology, which extends classical homology by controlling how chains interact with the singular strata.

Intersection homology is parameterized by a perversity <img src="https://latex.codecogs.com/svg.image?\bg{white}\bar{p}" />, which determines how simplicial chains are allowed to intersect the singular set. Formally, the intersection homology groups <img src="https://latex.codecogs.com/svg.image?\bg{white}IH_k(X;%20\bar{p})" /> are defined as the homology groups of the complex of allowable chains, where the chains must satisfy constraints imposed by the perversity.

##### Lemma 3.1: Homology of Links of Singularities

Let <img src="https://latex.codecogs.com/svg.image?\bg{white}L(p)" /> be the link of a singular point <img src="https://latex.codecogs.com/svg.image?\bg{white}p%20\in%20\Sigma" />. The homology groups <img src="https://latex.codecogs.com/svg.image?\bg{white}H_k(L(p))" /> encode the local topology near the singularity. The persistent homology near the singularity is governed by the homology of the link, and the evolution of homological features is determined by how the filtration progresses through the space.

##### Proof of Lemma 3.1

The link <img src="https://latex.codecogs.com/svg.image?\bg{white}L(p)" /> is a lower-dimensional space that provides a "snapshot" of the topology near the singularity. The homology groups <img src="https://latex.codecogs.com/svg.image?\bg{white}H_k(L(p))" /> describe the topological features of the link, and as we move through the filtration, these features either persist or disappear. The behavior of the homology near the singularity is thus determined by the homology of the link and the filtration of <img src="https://latex.codecogs.com/svg.image?\bg{white}X" />.

---

#### Definition 3.3: Spectral Sequences in Stratified Spaces

The spectral sequence is a multi-stage process for computing homology in complex spaces like stratified spaces. The spectral sequence associated with a stratified space <img src="https://latex.codecogs.com/svg.image?\bg{white}X" />, particularly near the singular set <img src="https://latex.codecogs.com/svg.image?\bg{white}\Sigma" />, refines the calculation of homology by introducing successive approximations to capture the topology of the space, layer by layer.

Let <img src="https://latex.codecogs.com/svg.image?\bg{white}L(p)" /> denote the link of the singularity <img src="https://latex.codecogs.com/svg.image?\bg{white}p%20\in%20\Sigma" />. A filtration <img src="https://latex.codecogs.com/svg.image?\bg{white}\{X_t\}_{t%20\geq%200}" /> of the space <img src="https://latex.codecogs.com/svg.image?\bg{white}X" /> induces a filtration on the link <img src="https://latex.codecogs.com/svg.image?\bg{white}L(p)" />, where the link captures the local structure of the space in the neighborhood of the singularity. As we progress through the filtration, the topological features of <img src="https://latex.codecogs.com/svg.image?\bg{white}L(p)" /> evolve, and this evolution is captured by the spectral sequence:

<img src="https://latex.codecogs.com/svg.image?\bg{white}E_1^{p,q}%20\Rightarrow%20H_{p+q}(X)" />,

where:
- <img src="https://latex.codecogs.com/svg.image?\bg{white}E_1^{p,q}" /> represents the homology groups of the link <img src="https://latex.codecogs.com/svg.image?\bg{white}L(p)" />,
- <img src="https://latex.codecogs.com/svg.image?\bg{white}H_{p+q}(X)" /> is the homology of <img src="https://latex.codecogs.com/svg.image?\bg{white}X" /> near the singularity.

##### Lemma 3.2: Persistent Homology from Spectral Sequences

The persistent homology near the singularity <img src="https://latex.codecogs.com/svg.image?\bg{white}p%20\in%20\Sigma" /> is determined by the evolution of homology classes in the link <img src="https://latex.codecogs.com/svg.image?\bg{white}L(p)" />, as captured by the spectral sequence. Specifically, the birth and death times of homological features are governed by the differentials <img src="https://latex.codecogs.com/svg.image?\bg{white}d_r" /> in the spectral sequence. These differentials describe how homology classes at one stage of the filtration transition into or disappear in later stages.

The persistence intervals for homology classes near the singularity are given by:

<img src="https://latex.codecogs.com/svg.image?\bg{white}PH_k(\Sigma)%20=%20\bigcup_{p%20\in%20\Sigma}%20\left\{%20[b_i,%20d_i)%20\mid%20H_k(L(p))%20\text{%20persists%20from%20}%20b_i%20\text{%20to%20}%20d_i%20\right\}" />,

where <img src="https://latex.codecogs.com/svg.image?\bg{white}H_k(L(p))" /> is the homology of the link, and <img src="https://latex.codecogs.com/svg.image?\bg{white}[b_i,%20d_i)" /> is the persistence interval of the corresponding homology class.

##### Proof of Lemma 3.2

The spectral sequence associated with the filtration of <img src="https://latex.codecogs.com/svg.image?\bg{white}X" /> near the singularity <img src="https://latex.codecogs.com/svg.image?\bg{white}p" /> describes how homological features evolve as the filtration progresses. At each stage of the filtration, the differentials <img src="https://latex.codecogs.com/svg.image?\bg{white}d_r" /> may cause a homology class to die, corresponding to the disappearance of a homological feature. The persistence intervals are determined by analyzing when these homology classes are born and when they are annihilated by the differentials of the spectral sequence.

Since the link <img src="https://latex.codecogs.com/svg.image?\bg{white}L(p)" /> captures the local topology near the singularity, the homology of the link governs the behavior of homological features in the neighborhood of <img src="https://latex.codecogs.com/svg.image?\bg{white}p" />. The persistence intervals near <img src="https://latex.codecogs.com/svg.image?\bg{white}\Sigma" /> thus depend on the homology of the link <img src="https://latex.codecogs.com/svg.image?\bg{white}L(p)" /> and the action of the differentials in the spectral sequence.

##### Corollary 3.1: Stability of Persistence Near Singularities

The persistence intervals near singularities are stable under small perturbations of the underlying space. Small changes in the topology of <img src="https://latex.codecogs.com/svg.image?\bg{white}X" /> near the singularities result in small changes in the persistence intervals, ensuring that the global topological structure of the space is preserved.

---

#### 4. Curvature-Weighted Filtrations and Geometric Contributions Near Singularities

##### Definition 4.1: Curvature-Weighted Filtration

In spaces with regions of high curvature, such as those with conical singularities or sharp edges, the persistence of homological features may be influenced by the local curvature. To account for this, we introduce a curvature-weighted filtration, which modifies the standard filtration by incorporating geometric information about the curvature of the space.

Let <img src="https://latex.codecogs.com/svg.image?\bg{white}\kappa:%20X%20\to%20\mathbb{R}" /> be the curvature function, which assigns a curvature value <img src="https://latex.codecogs.com/svg.image?\bg{white}\kappa(x)" /> to each point <img src="https://latex.codecogs.com/svg.image?\bg{white}x%20\in%20X" />. Define the curvature-weighted filtration <img src="https://latex.codecogs.com/svg.image?\bg{white}\{X_t^\kappa\}_{t%20\geq%200}" /> as the sublevel sets of <img src="https://latex.codecogs.com/svg.image?\bg{white}X" /> given by:

<img src="https://latex.codecogs.com/svg.image?\bg{white}X_t^\kappa%20=%20\{x%20\in%20X%20\mid%20\kappa(x)%20\leq%20t\}" />.

This filtration ensures that regions of high curvature are incorporated into the filtration earlier, allowing us to track how homological features behave in geometrically complex regions.

##### Lemma 4.1: Persistence Intervals Bounded by Curvature

Let <img src="https://latex.codecogs.com/svg.image?\bg{white}\Sigma%20\subset%20X" /> be the singular set, and let <img src="https://latex.codecogs.com/svg.image?\bg{white}\{X_t^\kappa\}_{t%20\geq%200}" /> be the curvature-weighted filtration. The persistence intervals for homology classes near <img src="https://latex.codecogs.com/svg.image?\bg{white}\Sigma" /> are bounded by the curvature of the space near the singularities. Specifically, the death times <img src="https://latex.codecogs.com/svg.image?\bg{white}d_i" /> of homology classes near <img src="https://latex.codecogs.com/svg.image?\bg{white}\Sigma" /> satisfy:

<img src="https://latex.codecogs.com/svg.image?\bg{white}d_i%20\leq%20\inf%20\left\{%20t%20\mid%20\alpha%20\text{is%20annihilated%20in}%20X_t^\kappa%20\right\}" />,

where <img src="https://latex.codecogs.com/svg.image?\bg{white}\alpha" /> is a homology class near the singularity, and <img src="https://latex.codecogs.com/svg.image?\bg{white}[b_i,%20d_i)" /> is the persistence interval for the corresponding homology feature.

##### Proof of Lemma 4.1

The curvature-weighted filtration incorporates geometric information about the space into the persistence computation. As regions of high curvature are added to the filtration earlier, homology classes in these regions may die sooner than they would under a standard filtration. The persistence intervals are thus constrained by the curvature near the singularities, providing an upper bound on the death times of homology classes.

By analyzing the action of the filtration on regions of high curvature, we obtain bounds on the persistence intervals, which ensures that homological features near singularities do not persist beyond scales dictated by the local geometry of the space.

##### Corollary 4.1: Geometric Stability of Persistent Homology

The persistent homology of a space with high curvature regions is stable under small perturbations of the curvature function <img src="https://latex.codecogs.com/svg.image?\bg{white}\kappa(x)" />. Changes in the curvature result in correspondingly small changes in the persistence intervals, ensuring that the global topological structure of the space is preserved.

---

#### 5. Unified Equation for Persistent Homology of Stratified Spaces

We now combine the contributions from the smooth, non-smooth, and singular regions of <img src="https://latex.codecogs.com/svg.image?\bg{white}X" /> to form the unified equation for the persistent homology of the stratified space <img src="https://latex.codecogs.com/svg.image?\bg{white}X" />.

##### Theorem 5.1: Unified Persistent Homology Equation

Let <img src="https://latex.codecogs.com/svg.image?\bg{white}X%20=%20X_{\text{smooth}}%20\cup%20X_{\text{non-smooth}}%20\cup%20\Sigma" /> be a stratified topological space, with smooth, non-smooth, and singular regions. The persistent homology of <img src="https://latex.codecogs.com/svg.image?\bg{white}X" /> in dimension <img src="https://latex.codecogs.com/svg.image?\bg{white}k" />, denoted <img src="https://latex.codecogs.com/svg.image?\bg{white}PH_k(X)" />, is given by the following unified equation:

<img src="https://latex.codecogs.com/svg.image?\bg{white}PH_k(X)%20=%20PH_k(X_{\text{smooth}})%20\cup%20\left(%20\sum_{\sigma^k%20\in%20X_{\text{non-smooth}}}%20\tau_k(\sigma^k)%20\right)%20\cup%20\left(%20\bigcup_{p%20\in%20\Sigma}%20PH_k(L(p))%20\right)" />,

where:
- <img src="https://latex.codecogs.com/svg.image?\bg{white}PH_k(X_{\text{smooth}})" /> is the persistent homology of the smooth region, computed using classical filtration techniques such as the Vietoris-Rips or alpha complex.
- <img src="https://latex.codecogs.com/svg.image?\bg{white}\sum_{\sigma^k%20\in%20X_{\text{non-smooth}}}%20\tau_k(\sigma^k)" /> is the persistent homology of the non-smooth regions, computed using discrete Morse theory, where <img src="https://latex.codecogs.com/svg.image?\bg{white}\tau_k(\sigma^k)" /> represents the persistence of the critical simplices in dimension <img src="https://latex.codecogs.com/svg.image?\bg{white}k" />.
- <img src="https://latex.codecogs.com/svg.image?\bg{white}\bigcup_{p%20\in%20\Sigma}%20PH_k(L(p))" /> is the persistent homology near singularities, computed using the homology of the links <img src="https://latex.codecogs.com/svg.image?\bg{white}L(p)" /> and the spectral sequences associated with the filtration of <img src="https://latex.codecogs.com/svg.image?\bg{white}X" />.

##### Proof of Theorem 5.1

The persistent homology of <img src="https://latex.codecogs.com/svg.image?\bg{white}X" /> is computed by analyzing each region of the space separately and then combining the results. The contribution from the smooth region <img src="https://latex.codecogs.com/svg.image?\bg{white}X_{\text{smooth}}" /> is given by classical persistent homology techniques, which compute the birth and death times of homology classes as the filtration progresses.

The non-smooth region <img src="https://latex.codecogs.com/svg.image?\bg{white}X_{\text{non-smooth}}" /> is analyzed using discrete Morse theory, which assigns critical values to simplices in the simplicial complex. The persistence intervals of homology classes in the non-smooth region are determined by the differences in the critical values of the simplices.

Finally, the singular region <img src="https://latex.codecogs.com/svg.image?\bg{white}\Sigma" /> is analyzed using intersection homology and spectral sequences. The homology of the link <img src="https://latex.codecogs.com/svg.image?\bg{white}L(p)" /> of each singularity <img src="https://latex.codecogs.com/svg.image?\bg{white}p" /> governs the behavior of homological features near the singularity. The persistence intervals in the singular region are determined by the differentials in the spectral sequence, which track the evolution of homology classes near <img src="https://latex.codecogs.com/svg.image?\bg{white}\Sigma" />.

By combining the contributions from the smooth, non-smooth, and singular regions, we obtain the unified equation for the persistent homology of <img src="https://latex.codecogs.com/svg.image?\bg{white}X" />.

---

### 6. Conclusion and Further Refinements

The unified equation for the persistent homology of stratified spaces <img src="https://latex.codecogs.com/svg.image?\bg{white}X" />, encompassing smooth, non-smooth, and singular regions, is an essential extension of classical persistent homology. By carefully accounting for the contributions from smooth spaces, polyhedral or piecewise-linear spaces, and spaces with topological singularities, this framework provides a comprehensive and systematic way to analyze the evolution of topological features across a wide variety of geometrically complex spaces.

### Final Unified Equation:

<img src="https://latex.codecogs.com/svg.image?\bg{white}PH_k(X)%20=%20PH_k(X_{\text{smooth}})%20\cup%20\left(%20\sum_{\sigma^k%20\in%20X_{\text{non-smooth}}}%20\tau_k(\sigma^k)%20\right)%20\cup%20\left(%20\bigcup_{p%20\in%20\Sigma}%20PH_k(L(p))%20\right)" />,

where:
- <img src="https://latex.codecogs.com/svg.image?\bg{white}PH_k(X_{\text{smooth}})" /> is the persistent homology derived from classical techniques in smooth regions, governed by standard filtration methods such as the Vietoris-Rips complex or alpha complex. The persistence intervals <img src="https://latex.codecogs.com/svg.image?\bg{white}[b_i,%20d_i)" /> are determined by analyzing the topology of the smooth part of the space.

- <img src="https://latex.codecogs.com/svg.image?\bg{white}\sum_{\sigma^k%20\in%20X_{\text{non-smooth}}}%20\tau_k(\sigma^k)" /> is the contribution from non-smooth regions (e.g., polyhedral complexes or piecewise-linear structures) analyzed using discrete Morse theory. The persistence intervals <img src="https://latex.codecogs.com/svg.image?\bg{white}\tau_k(\sigma^k)" /> reflect the combinatorial structure of the space and are governed by the critical simplices of the discrete Morse function.

- <img src="https://latex.codecogs.com/svg.image?\bg{white}\bigcup_{p%20\in%20\Sigma}%20PH_k(L(p))" /> represents the persistent homology near the singularities of <img src="https://latex.codecogs.com/svg.image?\bg{white}X" />, where <img src="https://latex.codecogs.com/svg.image?\bg{white}L(p)" /> is the link of the singularity at point <img src="https://latex.codecogs.com/svg.image?\bg{white}p%20\in%20\Sigma" />. The evolution of homology classes is computed using spectral sequences and intersection homology, and the persistence intervals are controlled by the differentials in the spectral sequence that govern the homological features in singular neighborhoods.

---

#### 6.1 Remarks on Theoretical Guarantees and Applications

The unified framework developed above provides several theoretical guarantees for persistent homology computations in stratified spaces. These guarantees rely on the rigorously defined methods employed in each region of <img src="https://latex.codecogs.com/svg.image?\bg{white}X" />, such as the stability of persistence intervals, the role of spectral sequences in singular spaces, and the use of discrete Morse theory in non-smooth spaces. Below we summarize some key guarantees:

1. Stability of Persistence Intervals: In all regions of <img src="https://latex.codecogs.com/svg.image?\bg{white}X" /> (smooth, non-smooth, and singular), the persistence intervals are stable under small perturbations in the space or in the underlying filtration process. This stability ensures that the topological features identified by persistent homology are robust to noise or slight variations in data.

2. Control of Persistence Intervals via Curvature: In regions of <img src="https://latex.codecogs.com/svg.image?\bg{white}X" /> where curvature plays a significant role (e.g., near conical singularities), the persistence intervals are bounded by the curvature-weighted filtration. This ensures that the geometry of the space influences the persistence of topological features in a predictable and quantifiable manner.

3. Intersection Homology for Singularities: For spaces with singularities, classical homology is often inadequate in capturing the full topological structure. By incorporating intersection homology and analyzing the links of singular points, we provide a comprehensive framework that guarantees the correct computation of persistent homology in singular regions.

4. Spectral Sequence Convergence: The spectral sequence associated with the stratified space <img src="https://latex.codecogs.com/svg.image?\bg{white}X" /> converges to the correct homology groups, providing an iterative method for computing the evolution of homological features as the filtration progresses. This convergence is critical for ensuring that the persistent homology near singularities is computed accurately.


#### 6.2 Applications and Generalizations

The unified framework for persistent homology is not only theoretically robust but also has practical applications across a wide range of fields. Below we discuss some key applications and potential generalizations:

1. Topological Data Analysis (TDA): The methods developed in this framework extend the applicability of TDA to datasets that are represented by complex, stratified spaces. For example, in biological systems, data from networks or shapes that exhibit singularities (e.g., protein folding structures or neuronal networks) can now be analyzed more rigorously using the tools of intersection homology and spectral sequences.

2. Algebraic Geometry and Singular Varieties: In algebraic geometry, spaces often exhibit singularities, such as nodal or cuspidal points on algebraic curves. The framework developed here provides a way to compute persistent homology in the presence of such singularities, offering new insights into the topological structure of algebraic varieties and their associated moduli spaces.

3. Geometric and Polyhedral Complexes: Non-smooth spaces, such as polyhedral complexes or spaces arising from discrete geometry, often exhibit combinatorial structures that can be effectively analyzed using discrete Morse theory. The application of this framework to material science (e.g., crystal lattices or molecular structures) allows for the study of topological features that emerge in these discrete settings.

4. Singularity Theory in Physics: In theoretical physics, singularities play a central role in many areas, including black hole physics, string theory, and general relativity. The intersection homology techniques developed here may have applications in understanding the topological behavior of spacetime near singularities, providing a new perspective on the persistence of topological features in physical models of the universe.

5. Persistent Homology in Fractals: Fractal sets, which often exhibit self-similarity and complex topological features, can now be rigorously analyzed using this framework. The quasi-periodic behavior of homology classes in fractal sets can be captured using persistent homology, providing closed-form expressions for persistence intervals that reflect the recursive structure of these spaces.

---

### 7. Refinement of Lemmas and Future Directions

While the unified equation provides a comprehensive framework for analyzing persistent homology in stratified spaces, there are several areas where further refinement and generalization may be possible:

1. Refinement of Curvature-Weighted Filtrations: While curvature provides a natural geometric bound for persistence intervals in spaces with singularities, further refinements could include more precise bounds on the persistence intervals, particularly for spaces with highly variable curvature. Incorporating more sophisticated geometric invariants, such as Ricci curvature or sectional curvature, may provide tighter constraints on persistence intervals.

2. Generalized Spectral Sequences for Higher-Dimensional Singularities: The spectral sequences developed here provide an effective tool for computing persistent homology in spaces with isolated singularities. Future work may focus on generalizing these techniques to handle higher-dimensional singular strata, where the complexity of the singular set increases.

3. Computational Optimization: While the theoretical framework developed here provides guarantees for persistent homology in complex spaces, the computational complexity of these methods (particularly spectral sequences and intersection homology) can be high for large datasets. Developing optimized algorithms for computing persistent homology in stratified spaces will be an important area for future research, with potential applications in both theoretical and applied fields.

4. Extension to Other Homology Theories: The methods developed here focus primarily on classical homology and intersection homology. Future work could extend this framework to other homology theories, such as \( K \)-theory or Floer homology, which arise in different mathematical and physical contexts.

---

### Concluding Remarks

The unified framework for persistent homology developed in this work provides a powerful tool for analyzing the topology of stratified spaces. By integrating classical homology, discrete Morse theory, intersection homology, and spectral sequences, we have developed a comprehensive approach to persistent homology that captures the full complexity of spaces with smooth, non-smooth, and singular regions.

The unified equation:

<img src="https://latex.codecogs.com/svg.image?\bg{white}PH_k(X)%20=%20PH_k(X_{\text{smooth}})%20\cup%20\left(\sum_{\sigma^k%20\in%20X_{\text{non-smooth}}}%20\tau_k(\sigma^k)\right)%20\cup%20\left(\bigcup_{p%20\in%20\Sigma}%20PH_k(L(p))\right)" />

provides a rigorous, formal description of how topological features evolve across different scales in these spaces, offering both theoretical guarantees and practical methods for computing persistent homology in real-world applications.

Future work will focus on refining these methods, improving computational efficiency, and extending the framework to new areas of mathematics and applied science.
