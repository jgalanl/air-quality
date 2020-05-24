# import graphviz

from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.metrics import confusion_matrix 
from sklearn.naive_bayes import GaussianNB

from db import extract_all_data

def decision_tree(train_data, target, test_data):
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(train_data, target)
    # r = tree.export_text(clf, feature_names=wine['feature_names'])
    # dot_data = tree.export_graphviz(clf, out_file=None)
    # graph = graphviz.Source(dot_data) 
    # graph.render("wine") 
    # print(r)

    predicted = clf.predict(test_data)

    return predicted
    # score = clf.score(test_data, test_target)

    # print("## Árbol de decisión \n")

    # print("Score: ", "{:.4f}".format(score))
    # print("Expected: ", test_target)
    # print("Predicted: ", predicted)

    # Evaluar el resultado generando una matriz de confusión. Calcular la precision, exactitud y sensibilidad para cada clase
    # cnf_matrix = confusion_matrix(test_target, predicted)
    # print("Confusion matrix: \n", cnf_matrix)

def predict():
    # Cargar todos los datos extrayendolos de la base de datos
    result = extract_all_data()
    total_data = result.val()

    # De lo extraido generamos 2 conjuntos: 1 con el target (IAQ class) y 1 con el data
    target = []
    train_data = []
    test_data = []
    dates = []

    for date in total_data:
        # print(date)
        daily_data = total_data[date]
        for hour in daily_data:
            # print(hour)
            hourly_data = daily_data[hour]

            # total data -> todo lo que hay en la base de datos
            # conjunto de entrenamiento: train data. Tiene el atributo air_quality_score
            # conjunto de test: predicted data: No tengan el air_quality_score

            if 'air_quality_score' in hourly_data:
                target.append(int(hourly_data["air_quality_score"]))
                train_data.append([hourly_data["clouds"], hourly_data["dew_point"],
                    hourly_data["feels_like"], hourly_data["humidity"], hourly_data["id"],
                    hourly_data["pressure"], hourly_data["temperature"], hourly_data["wind_deg"], hourly_data["wind_speed"]])
            else:
                test_data.append([hourly_data["clouds"], hourly_data["dew_point"],
                    hourly_data["feels_like"], hourly_data["humidity"], hourly_data["id"],
                    hourly_data["pressure"], hourly_data["temperature"], hourly_data["wind_deg"], hourly_data["wind_speed"]])
                
                dates.append([hourly_data["date"]])
      
    # Realizar predicción
    # train_data = train_test_split(train_data, target, train_size= 1, random_state=0)
    predicted = decision_tree(train_data, target, test_data)

    print(len(dates))
    print(len(predicted))

    # Recorrer lista de dates e ir insertando su valor de predicted en la base de datos - air_quality_predicted


    # Almacenar el resultado del predicted en Firebase dentro de su fecha y hora

if __name__ == "__main__":
    predict()