import h2o

class Estimator():
    def __init__(self,model):
        self.model = model
        self.h2omodel = None
        try:
            self.h2omodel = h2o.load_model(self.model.model_path)
        except:
            print(f"model cannot be loaded from {self.model.model_path}")
        self.prediction = None 
   
    def predict_for_dataframe(self,dataframe):
        if self.h2omodel is None:
            return None, None
        self.prediction = self.h2omodel.predict(dataframe)
        print(self.prediction)
        pred = self.prediction.as_data_frame().values
        # prediction and prediction error
        # return pred[:,0],pred[:,1]
        n = len(pred[:,0])
        return pred[:,0],[0.]*n

    # def __del__(self):
    #     print(self.h2omodel)
    #     try:
    #         if self.h2omodel is not None:
    #             h2o.remove(self.h2omodel)
    #         if self.prediction is not None:
    #             h2o.remove(self.prediction)
    #     except:
    #         print("problem with removing loaded model")
