# --------------
import pandas as pd
import scipy.stats as stats
import math
import numpy as np
import warnings

warnings.filterwarnings('ignore')
#Sample_Size
sample_size=2000

#Z_Critical Score
z_critical = stats.norm.ppf(q = 0.95)  


# path        [File location variable]


#Code starts here
data = pd.read_csv(path)

data_sample = data.sample(n=sample_size, random_state=0)

a = data_sample.installment


sample_mean = a.mean()
print('mean of sample = ',sample_mean)

sample_std = a.std()
print('std.dev = ',sample_std)

margin_of_error = (z_critical*sample_std)/(math.sqrt(sample_size))
print('moe = ',margin_of_error)

b  = sample_mean - margin_of_error
#print('confidence_interval[0] = ', round(confidence_interval,2))

c = sample_mean + margin_of_error

confidence_interval = [b,c]
print('confidence_interval = ', confidence_interval)

true_mean = data.installment.mean()
print('true mean of installment = ', round(true_mean,2))





# --------------
import matplotlib.pyplot as plt
import numpy as np

#Different sample sizes to take
sample_size=np.array([20,50,100])

#Code starts here
fig ,axes = plt.subplots(nrows=3, ncols=1)

for i in range(len(sample_size)):
    m = []
    for j in range(1000):
        a = data['installment'].sample(n=sample_size[i]).mean()
        m.append(a)
    mean_series = pd.Series(m)
    axes[i].hist(mean_series)
    plt.show()



# --------------
#Importing header files

from statsmodels.stats.weightstats import ztest

#Code starts here
a = data['int.rate']

float_int_rate = a.str.replace('%', ' ').astype(float)

data['int.rate'] = float_int_rate/100

z_statistic, p_value = ztest(data[data['purpose']=='small_business']['int.rate'], value=data['int.rate'].mean(), alternative='larger')

if (p_value < 0.05):
    inference = 'Reject'
else:
    inference = 'Accept'

print(inference)


# --------------
#Importing header files
from statsmodels.stats.weightstats import ztest

#Code starts here
z_statistic, p_value = ztest(data[data['paid.back.loan']=='No']['installment'], data[data['paid.back.loan']=='Yes']['installment'])

if (p_value < 0.05):
    inference = 'Reject'
else:
    inference = 'Accept'

print(inference)


# --------------
#Importing header files
from scipy.stats import chi2_contingency

#Critical value 
critical_value = stats.chi2.ppf(q = 0.95, # Find the critical value for 95% confidence*
                      df = 6)   # Df = number of variable categories(in purpose) - 1

#Code starts here

#yes = data.loc[data['paid.back.loan'] == "Yes"].groupby('paid.back.loan').count()[['purpose']]

y = data.loc[data['paid.back.loan'] == "Yes"]
yes = y['purpose'].value_counts().sort_index()
#yes  = yes.sort_values(['purpose'], inplace=True) 
##yes = yes.head(1)
print(yes)
n = data.loc[data['paid.back.loan'] == "No"]
no = n['purpose'].value_counts().sort_index() 
#no = no.head(1)
print(no)

#No = data.loc[data['paid.back.loan'] == "No"].groupby('paid.back.loan').count()[['purpose']]


observed = pd.concat([yes.transpose(), no.transpose()],keys=['Yes', 'No'],axis=1) 
print(observed)

#paid_back_loan = pd.qcut(data['paid.back.loan'], 2, labels = ['Yes', 'No'])

# make a frequency table with Land.Conotur
##observed = pd.crosstab(data['purpose'],paid_back_loan)

#print(observed)

# conduct the chi-square test with the above frequency table
chi2, p, dof, ex = stats.chi2_contingency(observed)

print("Chi-square statistic = ",chi2)
print("p-value = ",p)




#print (observed)

#chi2, p, dof, ex = chi2_contingency(observed, correction=False)
##print(dof, ex)

if (chi2 < critical_value):
    inference = 'Reject'
else:
    inference = 'Accept'

print(inference)








