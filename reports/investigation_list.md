# Investigation List

## What this list is for

This list contains the 20 stations that were ranked highest by the anomaly detection methods.

The ranking is meant to help the company decide which stations to check first. A high ranking does **not** mean that the station has stolen or deliberately lost fuel.

There can be other reasons for unexplained fuel differences, such as faulty equipment, temperature changes, recording errors, or problems with the data.

## Top 20 stations

| Rank | Station | Audit finding   | Avg unexplained litres/month | Estimated value/month (XAF) |
| ---: | ------- | --------------- | ---------------------------: | --------------------------: |
|    1 | ST-085  | Equipment fault |                        1,206 |                     979,781 |
|    2 | ST-045  | Confirmed loss  |                        1,727 |                   1,402,214 |
|    3 | ST-018  | No finding      |                        5,683 |                   4,615,400 |
|    4 | ST-043  | Not audited     |                        3,740 |                   3,037,233 |
|    5 | ST-103  | Not audited     |                        2,209 |                   1,794,318 |
|    6 | ST-023  | No finding      |                        3,812 |                   3,096,103 |
|    7 | ST-003  | Not audited     |                        2,312 |                   1,877,328 |
|    8 | ST-078  | Confirmed loss  |                        2,047 |                   1,662,433 |
|    9 | ST-026  | Not audited     |                        4,219 |                   3,426,794 |
|   10 | ST-122  | Not audited     |                        1,833 |                   1,488,682 |
|   11 | ST-110  | No finding      |                        4,515 |                   3,667,107 |
|   12 | ST-134  | Not audited     |                        3,963 |                   3,218,429 |
|   13 | ST-118  | No finding      |                        1,138 |                     924,014 |
|   14 | ST-006  | Confirmed loss  |                        2,402 |                   1,951,088 |
|   15 | ST-063  | Not audited     |                        2,090 |                   1,697,475 |
|   16 | ST-030  | No finding      |                        5,991 |                   4,865,466 |
|   16 | ST-091  | No finding      |                        6,237 |                   5,065,225 |
|   18 | ST-119  | Not audited     |                        4,727 |                   3,839,066 |
|   19 | ST-029  | Not audited     |                        1,865 |                   1,514,927 |
|   19 | ST-108  | Not audited     |                        3,349 |                   2,719,697 |

## What the audits showed

Out of the 20 stations:

* 3 had confirmed loss.
* 1 had an equipment fault.
* 6 had no finding.
* 10 had not been audited.

Looking only at the 10 stations that were audited, 3 were confirmed loss, 1 had an equipment fault, and 6 had no finding.

The 10 unaudited stations cannot be called either confirmed losses or false positives because there is no audit result for them.

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

The anomaly score should be treated as a reason to investigate, not as proof that someone is responsible for the loss.

## Estimated financial value

The average observed sales value in the dataset was about **812.14 XAF per litre**.

I used this value to estimate the monthly XAF value of the unexplained litres.

These XAF figures are only estimates. They do not mean that the station definitely lost or stole that amount of money.

## Important limitation

Only 46 of the 150 stations had audit results. This means the audit data cannot be treated as complete ground truth for the whole network.

The investigation list should therefore be used as a starting point for further checks.
