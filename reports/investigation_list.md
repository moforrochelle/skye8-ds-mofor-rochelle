# Investigation List

## What this list is for

This list contains the 20 stations that were ranked highest by the anomaly detection methods.

The ranking is meant to help the company decide which stations to check first. A high ranking does **not** mean that the station has stolen or deliberately lost fuel.

There can be other reasons for unexplained fuel differences, such as faulty equipment, temperature changes, recording errors, or problems with the data.

## Top 20 stations

| Rank | Station | Audit finding   | Avg positive unexplained litres/month | Estimated value/month (XAF) | Evidence / reason                                                                                            |
| ---: | ------- | --------------- | ------------------------------------: | --------------------------: | ------------------------------------------------------------------------------------------------------------ |
|    1 | ST-085  | Equipment fault |                                 1,206 |                     979,781 | Flagged by all three anomaly methods and ranked first overall; high fuel-level variability.                  |
|    2 | ST-045  | Confirmed loss  |                                 1,727 |                   1,402,214 | Flagged by all three methods and had the highest overall station loss percentage.                            |
|    3 | ST-018  | No finding      |                                 5,683 |                   4,615,400 | Strong agreement across methods with high fuel-level variability.                                            |
|    4 | ST-043  | Not audited     |                                 3,740 |                   3,037,233 | Flagged by all three methods and had a very high maximum fuel-specific loss.                                 |
|    5 | ST-103  | Not audited     |                                 2,209 |                   1,794,318 | Flagged by all three methods with high fuel-level variability.                                               |
|    6 | ST-023  | No finding      |                                 3,812 |                   3,096,103 | Flagged by all three methods with high fuel-level variability.                                               |
|    7 | ST-003  | Not audited     |                                 2,312 |                   1,877,328 | Flagged by all three methods and had a high maximum fuel-specific loss.                                      |
|    8 | ST-078  | Confirmed loss  |                                 2,047 |                   1,662,433 | Flagged by all three methods and had the highest maximum fuel-specific loss in the network.                  |
|    9 | ST-026  | Not audited     |                                 4,219 |                   3,426,794 | Flagged by all three methods with high overall and fuel-level anomaly measures.                              |
|   10 | ST-122  | Not audited     |                                 1,833 |                   1,488,682 | Appeared consistently in the combined anomaly ranking with elevated fuel-specific loss.                      |
|   11 | ST-110  | No finding      |                                 4,515 |                   3,667,107 | Strong agreement between anomaly methods despite a negative overall loss percentage.                         |
|   12 | ST-134  | Not audited     |                                 3,963 |                   3,218,429 | Appeared in the combined ranking with a high overall loss percentage.                                        |
|   13 | ST-118  | No finding      |                                 1,138 |                     924,014 | Flagged by anomaly methods with elevated overall and fuel-specific loss.                                     |
|   14 | ST-006  | Confirmed loss  |                                 2,402 |                   1,951,088 | Appeared consistently in the combined ranking and had an audit-confirmed loss finding.                       |
|   15 | ST-063  | Not audited     |                                 2,090 |                   1,697,475 | Appeared in the combined ranking because of its anomaly features despite a negative overall loss percentage. |
|   16 | ST-030  | No finding      |                                 5,991 |                   4,865,466 | High overall loss percentage and substantial estimated monthly positive unexplained volume.                  |
|   16 | ST-091  | No finding      |                                 6,237 |                   5,065,225 | Strong anomaly ranking and the highest estimated monthly positive unexplained volume among the top 20.       |
|   18 | ST-119  | Not audited     |                                 4,727 |                   3,839,066 | Appeared in the combined ranking with elevated loss and estimated monthly positive unexplained volume.       |
|   19 | ST-029  | Not audited     |                                 1,865 |                   1,514,927 | Appeared in the combined ranking with elevated fuel-specific loss variability.                               |
|   19 | ST-108  | Not audited     |                                 3,349 |                   2,719,697 | Strong anomaly ranking with elevated overall and fuel-specific loss measures.                                |

## What the audits showed

There were 46 audited stations in total:

* 5 confirmed loss
* 3 equipment fault
* 38 no finding

Out of the 20 stations in the investigation list:

* 3 had confirmed loss.
* 1 had an equipment fault.
* 6 had no finding.
* 10 had not been audited.

Looking only at the 10 stations that were audited in the top 20:

* 3 were confirmed loss.
* 1 had an equipment fault.
* 6 had no finding.

The 7 audited stations that were not confirmed loss should **not** be called false positives. An equipment fault is a different finding, and a "no finding" audit does not prove that the station could never have had an underlying measurement or loss issue.

The 10 unaudited stations cannot be classified as either confirmed losses or false positives because there is no audit result for them.

## Confirmed-loss stations

The five stations with confirmed loss in the audit data were checked against the full consensus ranking, not only the top 20.

Three of the five confirmed-loss stations appeared in the top 20 investigation list. The other two were ranked lower.

This shows that the anomaly ranking can identify some stations with confirmed loss, but it does not identify every confirmed-loss station at the highest ranks.

The audit results are also limited because only 46 of the 150 stations were audited.

## Why these stations should be investigated

The reasons in the table are based on the anomaly features and agreement between the different detection methods.

The three anomaly methods used were:

* Isolation Forest
* Local Outlier Factor
* Distance from the normal feature centre

Agreement between methods gives additional evidence that a station has an unusual pattern, but it does not prove the cause of that pattern.

Some stations also have negative overall loss percentages. These were kept in the analysis because negative unexplained differences can indicate measurement, recording, or reconciliation problems.

## What should happen next

The ranking should be used to decide where to investigate first.

For a station that appears high on the list, investigators should check:

* tank and dip-probe equipment
* manual and automatic tank readings
* temperature records
* delivery records
* tanker quantities
* pump readings
* sales records
* stock movements
* repeated loss patterns over time
* possible recording or data-entry problems

If an equipment problem is found, the station should not automatically be treated as a deliberate-loss case.

The anomaly score should be treated as a reason to investigate, not as proof that someone is responsible for the loss.

## Estimated financial value

The average observed sales value in the dataset was about **812.14 XAF per litre**.

This value was used to estimate the monthly XAF value of the **positive unexplained litres** for the top-ranked stations.

Only positive unexplained differences were included in this estimate. Negative differences were not treated as financial gains.

These XAF figures are estimates of the value associated with the unexplained volume. They do **not** mean that the station definitely lost or stole that amount of money.

For example, ST-045 had about **1,727 positive unexplained litres per month**, which gives an estimated value of about **1.40 million XAF per month** using the observed average sales value per litre.

## Important limitation

Only 46 of the 150 stations had audit results.

This means the audit data cannot be treated as complete ground truth for the whole network.

The investigation list is therefore a prioritisation tool. It should be used to decide which stations need further checks, rather than as a list of stations that are guilty of fuel theft or deliberate loss.

The final decision about a station should only be made after checking the physical equipment, records and operational evidence.
