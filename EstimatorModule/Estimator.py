import h2o

class Estimator():
    def __init__(self,model):
        self.model = model
        self.h2omodel = h2o.load_model(self.model.model_path)
        self.prediction = None 
   
    def predict_for_dataframe(self,dataframe):
        self.prediction = self.h2omodel.predict(dataframe)
        print(self.prediction)
        pred = self.prediction.as_data_frame().values
        # prediction and prediction error
        return pred[:,0],pred[:,1]
        
    def __del__(self):
        h2o.remove(self.h2omodel)
        if self.prediction is not None:
            h2o.remove(self.prediction)
