# import graphviz

from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.metrics import confusion_matrix 
from sklearn.naive_bayes import GaussianNB

from db import extract_all_data, insert_predicted

def naive_bayes(train_data, target, test_data, air_quality_score, air_quality_predicted):
    gnb = GaussianNB()
    gnb = gnb.fit(train_data, target)
    # r = tree.export_text(clf, feature_names=wine['feature_names'])
    # dot_data = tree.export_graphviz(clf, out_file=None)
    # graph = graphviz.Source(dot_data) 
    # graph.render("wine") 
    # print(r)

    predicted = gnb.predict(test_data)
    score = gnb.score(air_quality_score, air_quality_predicted)

    print("## Naive Bayes \n")

    print("Score: ", "{:.4f}".format(score))
    # print("Expected: ", test_target)
    # print("Predicted: ", predicted)

    return predicted
    # Evaluar el resultado generando una matriz de confusión. Calcular la precision, exactitud y sensibilidad para cada clase
    # cnf_matrix = confusion_matrix(test_target, predicted)
    # print("Confusion matrix: \n", cnf_matrix)

def predict():
    # Cargar todos los datos extrayendolos de la base de datos
    result = extract_all_data()
    total_data = result.val()

    # De lo extraido generamos 3 conjuntos: 1 con el target (Air Quality Score) y 2 con el data
        ## 1 conjunto data de entrenamiento: train data. Tiene el atributo air_quality_score
        ## 1 conjunto data de test: test data: No tienen el air_quality_score
    target = []
    train_data = []
    test_data = []
    dates = []
    air_quality_score = []
    air_quality_predicted = []

    for date in total_data:
        daily_data = total_data[date]
        for hour in daily_data:
            hourly_data = daily_data[hour]            

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

            if 'air_quality_score' in hourly_data and 'air_quality_predicted' in hourly_data:
                air_quality_score.append([hourly_data["air_quality_score"]])
                air_quality_predicted.append([hourly_data["air_quality_predicted"]])
      
    # Realizar predicción
    # train_data = train_test_split(train_data, target, train_size= 1, random_state=0)
    predicted = naive_bayes(train_data, target, test_data, air_quality_score, air_quality_predicted)

    # Recorrer lista de dates e ir insertando su valor de predicted en la base de datos
    for idx, date in enumerate(dates):
        insert_predicted(date[0], float(predicted[idx]))