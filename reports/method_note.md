# Method Note

## 1. Project goal

The goal of this project was to find stations that showed unusual fuel patterns and create a list of stations that should be investigated first.

The company has 150 stations and about 18 months of delivery, sales and tank-dip data.

There was no complete list of stations known to have lost fuel. Only 46 stations had audit results.

Because of this, the project was treated as an anomaly detection problem rather than a normal classification problem.

## 2. Data used

The main datasets were:

* 150 stations
* 19,988 delivery records
* 246,100 sales records
* 246,000 tank-dip records
* 46 audit records

The dates were written in different formats, so they were converted to one date format before joining the datasets.

There were also repeated tank readings for some station, date and fuel combinations. These were combined into daily readings.

## 3. Calculating unexplained loss

For each station, fuel type and day, I calculated:

**Opening stock + deliveries - sales - closing stock**

This gave the unexplained fuel difference in litres.

I also calculated throughput as:

**Sales + deliveries**

The loss percentage was then:

**Unexplained loss / throughput × 100**

The calculations were also done over the full period and by month.

A negative unexplained value was kept because it can tell us something about measurement or reconciliation problems. It was not automatically treated as zero loss.

## 4. Features used

At station level, I created features such as:

* overall loss percentage
* loss variability
* percentage of days with positive unexplained loss
* average fuel-specific loss
* fuel-specific loss variability
* maximum fuel-specific loss

I also checked whether temperature was related to unexplained loss.

The correlation was about **-0.002**, which is basically zero in this dataset.

This does not mean temperature can never affect tank measurements. It only means that we did not see a useful linear relationship between the available temperature and loss data.

## 5. Anomaly detection methods

I used three different approaches:

1. Isolation Forest
2. Local Outlier Factor
3. Distance from the normal feature centre

The methods did not produce exactly the same ranking.

Seven stations appeared in the top 10 for both Isolation Forest and LOF.

I combined the results from the different methods to create the final top 20 investigation list.

I also used K-Means to look at possible groups of stations. The best silhouette score was for **3 clusters**, but the score was only about **0.224**, so the clusters were not very strongly separated.

Because of this, clustering was used mainly to understand the data and not as the main way of deciding which stations were suspicious.

## 6. Checking the ranking with audits

There were 46 audit records:

* 5 confirmed loss
* 3 equipment fault
* 38 no finding

In the final top 20:

* 3 were confirmed loss
* 1 had an equipment fault
* 6 had no finding
* 10 had not been audited

Among the 10 audited stations in the top 20, 3 were confirmed loss and 7 were not confirmed loss.

The 7 should not be called false positives because one had an equipment fault and six had no finding.

The 10 unaudited stations also cannot be classified because there is no audit result for them.

## 7. Supervised model

I also tested a Gradient Boosting model using the audited stations.

Only confirmed loss and no finding were used as labels. Equipment-fault stations were left out rather than treating them as normal stations.

There were only 5 confirmed-loss stations, so the supervised results have a lot of uncertainty.

The tuned model had:

* Average Precision: about **0.648**
* ROC-AUC: about **0.953**

Repeated cross-validation showed that the results could change quite a lot between samples. This is mainly because there were only 5 positive cases.

The supervised and unsupervised top 20 lists had 7 stations in common.

Because the audit sample was small, the supervised model was not treated as the final truth for the whole network.

## 8. Checking different station groups

I also checked whether the results were different by:

* brand
* region
* highway site
* manager tenure

I used the Kruskal-Wallis test because the loss percentages were not assumed to follow a normal distribution.

The results were:

| Factor         | p-value |
| -------------- | ------: |
| Brand          |  0.8060 |
| Region         |  0.0200 |
| Highway site   |  0.3278 |
| Manager tenure |  0.2282 |

Region had an overall p-value below 0.05.

I then compared the regions pair by pair using Mann-Whitney tests and applied a Holm correction because there were many comparisons.

After the correction, none of the individual regional comparisons remained significant at the 0.05 level.

So the analysis shows an overall difference between regions, but it does not give enough corrected evidence to say that one particular region is different from another.

The other three factors did not show a statistically significant overall difference.

## 9. Confidence intervals

I used bootstrap confidence intervals to show the uncertainty around the average loss percentage for each group.

These intervals are useful because some groups have relatively few stations.

The intervals should be used to understand the uncertainty in the estimates, not as proof that one group causes more loss than another.

## 10. Estimated monthly value

The average sales value in the dataset was about **812.14 XAF per litre**.

I used this value to estimate the XAF value of the positive unexplained litres for the top-ranked stations.

For example, ST-045 had about **1,727 unexplained litres per month**, which is approximately **1.40 million XAF per month** using the observed value per litre.

This is only an estimate. It should not be treated as confirmed financial loss.

## 11. False accusation risk

One of the main risks in this project is treating an unusual station as guilty without checking the reason for the unusual result.

An unexplained fuel difference can come from:

* faulty tank equipment
* temperature effects
* tank measurement problems
* recording errors
* delivery or sales data problems
* normal operational differences

ST-085 is a good example. It ranked first but its audit found an equipment fault rather than confirmed loss.

This shows why the ranking should be used to decide where to investigate, rather than to accuse a station or employee.

## 12. What should be checked during an investigation

Before making a decision about a station, investigators should check:

* tank-probe calibration
* manual and automatic dip readings
* temperature records
* delivery documents
* tanker quantities
* pump readings
* sales records
* stock movements
* repeated patterns over time
* possible data-entry problems

The anomaly ranking should be combined with these checks before reaching a final conclusion.

## 13. Limitations

There are several limitations to this analysis:

1. Only 46 of the 150 stations had audit results.
2. Only 5 audited stations were confirmed loss.
3. Equipment faults were not treated as normal negative cases.
4. The audit data are not complete ground truth for all stations.
5. Tank measurements and data recording can introduce noise.
6. The three anomaly methods did not always agree.
7. The supervised model had very few positive examples.
8. The XAF estimates depend on the observed average sales value per litre.

For these reasons, the final ranking should be treated as a way to prioritise investigations, not as proof of fuel theft or deliberate loss.
