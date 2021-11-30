# rpc-currents-ml
This package is intended for use in the study and monitoring of CMS RPC currents. 
It implements two types of Machine Learning algorithms: Generalized Linear Models and Autoencoders. The goal in both cases is to use the data available on the behavior of RPC currents in order to be able to train the models based on the above algorithms, thus characterizing this behavior, and be able to predict the currents for future points in time.









indexes to be created
CREATE INDEX TrainingData_DPID_IDX USING BTREE ON RPCCURRML.TrainingData (DPID,CHANGE_DATE); 
CREATE INDEX PredictedCurrent_predicted_for_IDX USING BTREE ON RPCCURRML.PredictedCurrent (predicted_for,model_id);
