from libs import *
import yaml

with open('config.yml', 'r') as yml:
    config = yaml.safe_load(yml)

update_data.UpdateDataLoto6(config).update()
update_data.UpdateDataLoto7(config).update()

predict = loto_predict.Loto6Predict(config)
print(predict.predict())

predict = loto_predict.Loto7Predict(config)
print(predict.predict())
