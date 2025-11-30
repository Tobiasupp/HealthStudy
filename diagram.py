import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def blodtryck_ålder(df):  

    """BarDiagram för genomsnittligt blodtryck per åldersgrupp"""
    
    age_bins = [18, 30, 45, 60, 75, 120]
    age_labels = ["18–30", "31–45", "46–60", "61–75", "76+"]

    df["age_group"] = pd.cut(df["age"], bins=age_bins, labels=age_labels, right=False)

    # Beräkna medelvärde för varje grupp
    bp_means = df.groupby("age_group", observed=False)["systolic_bp"].mean()

    # Rita diagrammet
    plt.bar(bp_means.index.astype(str), bp_means.values)

    plt.xlabel("Åldersgrupper")
    plt.ylabel("Genomsnittligt blodtryck")
    plt.title("Genomsnittligt blodtryck per åldersgrupp")
    plt.xticks(rotation=45)
    plt.grid(axis = "x")
    plt.tight_layout()
    plt.show()


def viktKM(df):
    """Boxplot för vikt per kön"""


    female_weight = df.loc[df["sex"] == "F", "weight"]
    male_weight = df.loc[df["sex"] == "M", "weight"]

    plt.boxplot([female_weight, male_weight], tick_labels=["Female", "Male"])
    plt.title("Vikt per kön")
    plt.ylabel("Vikt")
    plt.tight_layout()
    plt.show()


def ålderSkillnad(df):

    """Histogram för åldersfördelning på antal personer i undersökning"""

    plt.hist(df["age"], bins=50)
    plt.title("Åldersfördelning")
    plt.xlabel("Ålder")
    plt.ylabel("Antal personer")
    plt.show()

def genderBMISickness(df):
    """
    Räknar ut bmi för att sedan använda det i en boxplott som delar upp kön, sedan delas kön upp i sjukdom och icke sjukdom sen jämförs det med BMI
    """

    df['BMI'] = df['weight'] / ((df['height']/100)**2)  
    
    positions = [1,2,4,5]  # Positioner för boxarna
    colors = {'M': 'blue', 'F': 'red'}
    
    data_to_plot = [
        df[(df['disease']==0) & (df['sex']=='M')]['BMI'],
        df[(df['disease']==0) & (df['sex']=='F')]['BMI'],
        df[(df['disease']==1) & (df['sex']=='M')]['BMI'],
        df[(df['disease']==1) & (df['sex']=='F')]['BMI']
    ]
    box = plt.boxplot(data_to_plot, positions=positions, widths=0.6, patch_artist=True)

    
    for patch, color in zip(box['boxes'], ['blue','red','blue','red']):
        patch.set_facecolor(color)
        patch.set_alpha(0.2)  

    plt.xticks([1.5,4.5], ['No Disease','Disease'])
    plt.title('BMI fördelat efter sjukdom och kön')
    plt.ylabel('BMI')
    plt.grid(True, axis='y')

    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='blue', alpha=0.5, label='Man'),
                    Patch(facecolor='red', alpha=0.5, label='Kvinna')]
    plt.legend(handles=legend_elements, title='Kön')

    plt.show()