Fitting tool data to Reliability Distributions

  - Weibul

  - Lognormal

  - Gamma

----

## Emperical Lifetime Distribution

### Observed Tool Lifetime Distribution (Hours & Cycles)

``` vegalite
--8<-- "docs/trace-or/tool-lifetime.json"
```
*This shows how long tools actually survive in the field, revealing real-world variability across days-to-years lifetimes.*




## Model Fit Comparison

### Reliability Model Fit Comparison (Weibull vs Lognormal vs Gamma)

``` vegalite
--8<-- "docs/trace-or/cdf-curves.json"
```
*Multiple reliability models are overlaid to identify which statistical form best represents observed failure behavior.*



## Failure Probability Over Time

### Probability of Failure vs Time in Service

``` vegalite
--8<-- "docs/trace-or/tool-lifetime-fitted.json"
```
*These curves quantify how failure risk evolves as tools age, highlighting
early-life, random, and wear-out behavior.*

## Hazard Rate / Risk Acceleration

### Failure Hazard Rate and Risk Acceleration

``` vegalite
--8<-- "docs/trace-or/hazard-rate.json"
```
*The hazard rate reveals when failure risk begins to accelerate, defining
practical intervention and replacement windows.*

## Cost-Weighted Failure Risk

### Expected Cost Exposure Over Time (Cost-Weighted Risk)

``` vegalite
--8<-- "docs/trace-or/cost-weighted-risk.json"
```
*By translating failure probability into dollars, this view shows when continued
operation becomes economically irrational.*

## Foundational View — Empirical Data + Reliability Context

### Observed Tool Lifetimes with Reliability Context Overlay

``` vegalite
--8<-- "docs/trace-or/prob-fail-dist.json"
```
*This combined view anchors the analysis by showing raw observed tool lifetimes
alongside reliability context, illustrating why probabilistic modeling is
required instead of point estimates.*




