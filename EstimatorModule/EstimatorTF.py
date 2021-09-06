from tensorflow import keras



class EstimatorTF():
    def __init__(self,model):
        self.model = model
        self.kerasmodel = None
        try:
            self.kerasmodel = keras.load_model(self.model.model_path)
        except:
            print(f"model cannot be loaded from {self.model.model_path}")
        self.prediction = None 
   
    def predict_for_dataframe(self,dataarray):
        if self.kerasmodel is None:
            return None, None
        self.prediction = self.kerasmodel.predict(dataarray)
        print(self.prediction)
        # pred = self.prediction.as_data_frame().values
        # prediction and prediction error
        # return pred[:,0],pred[:,1]
        n = len(self.prediction[:])
        return self.prediction[:],[0.]*n
