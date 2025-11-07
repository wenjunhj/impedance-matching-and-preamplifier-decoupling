# Usage
The configuration of this preamplifier decoupling/gain and impedance matching network calculator is illustrated below. <br/>
<img src="../assets/preamplifier_decoupling_configuration.png" alt="Preamplifier Decoupling Configuration" width="500" />

For this program, it is assumed that: 
- All inductors are capacitors are ideal.
- All resistance values are positive.
- All values are finite.

## Three- and Four-Element Matching Networks for High or Low Impedance
This function is fulfilled by `three_element_network.ipynb`, `four_element_network.ipynb`, and the associated Python files.
### Cases
Use the high-impedance case "HZ" to: 
- Suppress the loop current of a loop MRI coil (i.e. an electrically small loop antenna). In this case, 
    - Set $`Z_\mathrm{coil}`$ as the coil impedance. A rough coil reactance and a rough estimation of the coil resistance will usually make a decent initial design.
    - Set $`Z_\mathrm{out}`$ as the optimal noise impedance of the preamplifier module.
    - Set $`Z_\mathrm{amp}`$ as the input impedance of the preamplifier module.
    - $`Z_\mathrm{in}`$ will be automatically calculated.

In theory, the high-impedance case "HZ" is valid when $`X_{\mathrm{amp}}+X_{\mathrm{out}}\neq 0`$ or $`R_{\mathrm{out}} > R_{\mathrm{amp}} \geq 0`$. When the condition of validity is not met, an impedance transform network does not exist. An example can be found [here](../docs/Example_of_Impossible_Matching.md).

In the implementation, it is required that $`R_{\mathrm{amp}} > 0`$, i.e., the condition of validity is $`X_{\mathrm{amp}}+X_{\mathrm{out}}\neq 0`$ or $`R_{\mathrm{out}} > R_{\mathrm{amp}} > 0`$. 

Use the low-impedance case "LZ" to: 
- Design a preamplifier that has a real $`Z_\mathrm{opt}`$ and a low input impedance $`Z_\mathrm{amp}`$. In this case:
    - Set $`Z_\mathrm{coil}`$ as the target optimal noise impedance, e.g. $`Z_\mathrm{coil}=50~\Omega`$, or anything you need.
    - Set $`Z_\mathrm{out}`$ as the optimal noise impedance of the "true" amplifier, i.e. the optimal noise impedance seen at the input of the very first transistor stage.
    - Set $`Z_\mathrm{amp}`$ as the input impedance of the "true" amplifier, i.e. the input impedance seen at the input of the very first transistor stage.
    - $`Z_\mathrm{in}`$ will be automatically calculated.
- Suppress the loop current of a multi-turn multi-gap high-impedance coil made of a coaxial cable (i.e. a shielded loop at fundamental resonance). A rough coil reactance and a rough estimation of the coil resistance will usually make a decent initial design.
    - Set $`Z_\mathrm{coil}`$ as the coil impedance. A rough coil reactance and a rough estimation of the coil resistance will usually make a decent initial design.
    - Set $`Z_\mathrm{out}`$ as the optimal noise impedance of the preamplifier module.
    - Set $`Z_\mathrm{amp}`$ as the input impedance of the preamplifier module.
    - $`Z_\mathrm{in}`$ will be automatically calculated.

The low-impedance case "LZ" is valid when  $`X_{\mathrm{amp}}+X_{\mathrm{out}}\neq 0`$ or $`R_{\mathrm{amp}} > R_{\mathrm{out}} > 0`$.
### Results
For each valid combination of $`Z_\mathrm{coil}`$, $`Z_\mathrm{out}`$, $`Z_\mathrm{amp}`$, and case, there will be in total **4 solutions** for three-element matching (impedance transform) networks.

For each valid combination of $`Z_\mathrm{coil}`$, $`Z_\mathrm{out}`$, $`Z_\mathrm{amp}`$, and case, there will be an infinite number of solutions for four-element matching (impedance transform) networks. The resulting networks should be filtered so that they contain realistic component values.
## Preamplifier Decoupling/Gain vs Noise Figure Trade-Off
This function is fulfilled by `preamplifier_decoupling_and_gain_vs_noise_figure.ipynb`. Currently calculate at a single frequency point is supported. 
Put in these numbers and run the notebook: 
- The S parameters
- The noise parameters including minimum noise figure, $`R_{n}`$, $`S_{\mathrm{opt}}`$ (i.e. $`\Gamma_{\mathrm{opt}}`$). 
