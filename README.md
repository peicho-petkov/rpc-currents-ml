# rpc-currents-ml

indexes to be created
CREATE INDEX TrainingData_DPID_IDX USING BTREE ON RPCCURRML.TrainingData (DPID,CHANGE_DATE); 
CREATE INDEX PredictedCurrent_predicted_for_IDX USING BTREE ON RPCCURRML.PredictedCurrent (predicted_for,model_id);
