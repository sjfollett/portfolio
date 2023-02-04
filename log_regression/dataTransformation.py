import pandas as pd


def mapGradeToScore(x):
    score = 625
    if "A" in x:
        score += 150
    if "B" in x:
        score += 125
    if "C" in x:
        score += 100
    if "D" in x:
        score += 75
    if "E" in x:
        score += 50
    if "F" in x:
        score += 25
    if "G" in x:
        score += 0

    if "1" in x:
        score += 20
    if "2" in x:
        score += 15
    if "3" in x:
        score += 10
    if "4" in x:
        score += 5
    if "5" in x:
        score += 0

    return score


def mapPurpose(x):
    if"credit_card" in x:
        return "debt_consolidation"
    if"home_improvement" in x:
        return "house"
    if"renewable_energy" in x:
        return "house"
    if"car" in x:
        return "major_purchase"
    if"vacation" in x:
        return "major_purchase"
    if"wedding" in x:
        return "major_purchase"
    return x


df = pd.read_csv("Data/150KData.csv", skipinitialspace=True)
df['creditScore'] = df.apply(lambda row: mapGradeToScore(row['sub_grade']), axis=1)
df['creditPurpose'] = df.apply(lambda row: mapPurpose(row['purpose']), axis=1)
df.drop(['sub_grade', 'purpose'], axis=1, inplace=True)
df.to_csv("Data/150K.csv")
print(df.head())
