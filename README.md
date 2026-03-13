# spring-2026-predicting-streetcar-delays
Team project: spring-2026-predicting-streetcar-delays
# Route 506 Streetcar Bunching vs Delay Overview

## 1. Objective: 

The primary goal is to understand the relationship between **streetcar bunching incidents** and **accumulated delay time** on TTC route 506. 

In particular, we investigate the impact of bunching incidents on delay times while controlling for: 
- **time of day**
- **time of week** (Weekday, Saturday, or Sunday) 


-- 

### What is a bunching incident? 

A **bunching incident** occurs when two streetcars on the same route travel too closely together instead of maintaining even spacing along the route. 

In contrast, a **gapping incident** occurs when the time between consecutive streetcars becomes unusually large.

For Route 506: 

- The **scheduled headway** between vehicles is approximately 10 minutes. 

- This means ideally, vehicles should arrive at stops in 10 minute intervals. 

- A **bunching incident** occurs when the **actual headway** between two vehicles becomes much smaller than the **scheduled headway**. 

- For this analysis, a bunching incident is defined as 
> **ACTUAL HEADWAY < X minutes**

### Why bunching matters? 

Bunching often starts a cascade of problems which impact operations along an entire transit route. 

A typical sequence of events is:

1. A bunching incident occurs.
2. The gap to the following vehicle increases.
3. More passengers accumulate at the stops in between.
4. Boarding times increase due to congestion.
5. The following vehicle has fewer passengers and travels faster.
6. More vehicles begin to bunch and the cycle continues. 

This creates two major service problems: 
- **Increased wait times** for passengers in the gaps
- **Congestion and overcrowding** for the vehicles arriving after the gap

As a result, even when vehicles arrive exactly at the scheduled time, if there is poor headway adherance the service feels unreliable for the passenger.  


### Research Question

This analysis addresses the following question:

> **How does the number of bunching incidents affect accumulated delay time on Route 506?**

In particular, we aim to quantify the relationship between bunching and delay in order to estimate:

- how delay increases as bunching increases
- how reducing bunching might improve service reliability

## 2. The Data

This data comes from TTC. 

Each entry provides different service statistics related to the 506 streetcar line for a specified time period on a given day.  

To model the relationship we use data for dates in the range:
 ==START DATE - END DATE== 


## Key Variables

The primary goal of this analysis is to study the relationship between **number of bunching incidents** and **total accumulated delay time**. 

We also include **gapping** as a variable in our analysis because **bunching** and **gapping** are closely related operational features. A bunch is often followed by a gap or vice versa, and so together they both influence the spacing between vehicles along the route. However, the main focus of this analysis will remain on **bunching incidents**.


A similar modeling framework could also be used to study the relationship between **gapping** and **delay**.

| Variable | Description |
|--------|-------------|
| **`bunch`** | A count of the number of bunching incidents that occurred within the specified time period. |
| **`gap`** | A count of the number of gapping incidents that occurred within the specified time period. |
| **`total delay`** | Sum of the total accumulated delay time (in minutes) for all streetcars on the route during the same time period. |

In this analysis, **bunching** will be treated as the main variable of interest. 

Initial analysis shows that there is a positive correlation between the number of bunching and gapping incidents in a given time period. To avoid potential problems with colinearity we will not include **gapping** as a feature in the model. 


## Additional Variables

To account for predictable variations in service along the route, we also include the following variables. 



| Variable | Description |
|----------|-------------|
| **`weekday`** | Categorical variable indicating the **type of day** 
| **`time_period`** | Categorical variable indicating the **time of day service block** for the entry.|  


The `weekday` variable is interpreted as:

- **0** = Weekday  
- **1** = Saturday  
- **2** = Sunday  


The `time_period` variable divides the service day into five consecutive blocks determined by TTC defines time periods which are encoded as follows:  

For Weekdays: 
| `time_period` | Approximate interval | Description |
|---------------|----------------------|-------------|
| **0** | 4:00 AM - 9:00 AM | morning peak |
| **1** | 9:00 AM - 3:00 PM | midday |
| **2** | 3:00 PM - 7:00 PM | afternoon peak|
| **3** | 7:00 PM - 10:00 PM | early evening |
| **4** | 10:00 PM - 4:00 AM | late evening |

For Saturday and Sunday:
| `time_period` | Approximate interval | Description |
|---------------|----------------------|-------------|
| **0** | 4:00 AM - 8:00 AM | morning peak |
| **1** | 8:00 AM - 12:00 PM | morning |
| **2** | 12:00 PM - 7:00 PM | afternoon |
| **3** | 7:00 PM - 10:00 PM | early evening |
| **4** | 10:00 PM - 4:00 AM | late evening |

These variables are included as controls because variations in ridership and congestion are likely to vary significantly depending on the time of day and day of the week. Controlling for these variables helps ensure that any relationship we observe between bunching and delay is not simply due to predictable daily patterns. 



