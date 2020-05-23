import graphviz

from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.metrics import confusion_matrix 
from sklearn.naive_bayes import GaussianNB

from db import extract_all_data

def decision_tree(train_data, test_data, train_target, test_target):
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(train_data, train_target)
    # r = tree.export_text(clf, feature_names=wine['feature_names'])
    # dot_data = tree.export_graphviz(clf, out_file=None)
    # graph = graphviz.Source(dot_data) 
    # graph.render("wine") 
    # print(r)

    predicted = clf.predict(test_data)
    score = clf.score(test_data, test_target)

    print("## Árbol de decisión \n")

    print("Score: ", "{:.4f}".format(score))
    print("Expected: ", test_target)
    print("Predicted: ", predicted)

    # Evaluar el resultado generando una matriz de confusión. Calcular la precision, exactitud y sensibilidad para cada clase
    cnf_matrix = confusion_matrix(test_target, predicted)
    print("Confusion matrix: \n", cnf_matrix)

def predict():
    # Cargar todos los datos extrayendolos de la base de datos
    result = extract_all_data()
    total_data = result.val()

    # De lo extraido generamos 2 conjuntos: 1 con el target (IAQ class) y 1 con el data
    target, data = [], []
    for date in total_data:
        print(date)
        daily_data = total_data[date]
        for hour in daily_data:
            print(hour)
            hourly_data = daily_data[hour]
            if (len(hourly_data) == 18): # That means there are sensor data & api data
                target.append(hourly_data["iaq_class"])
                data.extend([[hourly_data["air_quality_score"], hourly_data["clouds"], hourly_data["date"], hourly_data["description"],
                    hourly_data["dew_point"], hourly_data["feels_like"], hourly_data["gas_resistance_sensor"],
                    hourly_data["humidity"], hourly_data["humidity_sensor"], hourly_data["id"], hourly_data["main"],
                    hourly_data["pressure"], hourly_data["pressure_sensor"], hourly_data["temperature"], hourly_data["temperature_sensor"],
                    hourly_data["wind_deg"], hourly_data["wind_speed"]]])
            elif (len(hourly_data) == 12): # That means there aren't sensor data, only api data
                data.extend([[hourly_data["clouds"], hourly_data["date"], hourly_data["description"], hourly_data["dew_point"],
                    hourly_data["feels_like"], hourly_data["humidity"], hourly_data["id"], hourly_data["main"],
                    hourly_data["pressure"], hourly_data["temperature"], hourly_data["wind_deg"], hourly_data["wind_speed"]]])

    # print(target)
    # print(data)

    # Realizar predicción
    # train_data, test_data, train_target, test_target = train_test_split(data, target, test_size=0.3, random_state=0)

    # decision_tree(train_data, test_data, train_target, test_target)

    # Almacenar el resultado del predicted en Firebase dentro de su fecha y hora

if __name__ == "__main__":
    predict()