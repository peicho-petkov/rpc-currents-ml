from .base import *
from .db_tables import *

table_training = db_tables.TrainingDataTable()
table_uxcenv = db_tables.UxcEnvTable()
table_lumi = db_tables.LumiDataTable()
table_mlmodelsconf = db_tables.MLModelsConf()
table_mlmodels = db_tables.MLModels()
table_predicted_current = db_tables.PredictedCurrentsTable()
table_configuration = db_tables.ConfigurationTable()
table_notifications = db_tables.NotificationsTable()
table_dpidstates = db_tables.dpidStateTable()

#rpccurrml = mysql_dbConnector(host='localhost',user='ppetkov',password='Fastunche')
#rpccurrml.connect_to_db('RPCCURRML')
#rpccurrml.self_cursor_mode()

automation_db = oracle_dbConnector(user='CMS_RPC_PVSS_TEST', password='rpcr22_d3Own') #, dsn_tns="./tnsnames.ora")
automation_db.connect_to_db(database='int2r_nolb')
automation_db.self_cursor_mode()

#omds = oracle_dbConnector(user='cms_rpc_test_r',password='rpcr20d3R')
#omds.connect_to_db('cman_int2r')

dpid_colnames = [  'dpid315',
  'dpid316',
  'dpid317',
  'dpid318',
  'dpid319',
  'dpid320',
  'dpid322',
  'dpid323',
  'dpid324',
  'dpid325',
  'dpid326',
  'dpid327',
  'dpid329',
  'dpid330',
  'dpid331',
  'dpid332',
  'dpid333',
  'dpid334',
  'dpid336',
  'dpid337',
  'dpid338',
  'dpid339',
  'dpid340',
  'dpid341',
  'dpid343',
  'dpid344',
  'dpid345',
  'dpid346',
  'dpid347',
  'dpid348',
  'dpid350',
  'dpid351',
  'dpid352',
  'dpid353',
  'dpid354',
  'dpid355',
  'dpid357',
  'dpid358',
  'dpid359',
  'dpid360',
  'dpid361',
  'dpid362',
  'dpid364',
  'dpid365',
  'dpid366',
  'dpid367',
  'dpid368',
  'dpid369',
  'dpid371',
  'dpid372',
  'dpid373',
  'dpid374',
  'dpid375',
  'dpid376',
  'dpid378',
  'dpid379',
  'dpid380',
  'dpid381',
  'dpid382',
  'dpid383',
  'dpid385',
  'dpid386',
  'dpid387',
  'dpid388',
  'dpid389',
  'dpid392',
  'dpid393',
  'dpid394',
  'dpid395',
  'dpid396',
  'dpid397',
  'dpid399',
  'dpid400',
  'dpid401',
  'dpid402',
  'dpid403',
  'dpid404',
  'dpid406',
  'dpid407',
  'dpid408',
  'dpid409',
  'dpid410',
  'dpid411',
  'dpid413',
  'dpid414',
  'dpid415',
  'dpid416',
  'dpid417',
  'dpid418',
  'dpid420',
  'dpid421',
  'dpid423',
  'dpid424',
  'dpid425',
  'dpid2928',
  'dpid2929',
  'dpid2930',
  'dpid2931',
  'dpid2932',
  'dpid2933',
  'dpid2935',
  'dpid2936',
  'dpid2937',
  'dpid2938',
  'dpid2939',
  'dpid2940',
  'dpid2942',
  'dpid2943',
  'dpid2944',
  'dpid2945',
  'dpid2946',
  'dpid2947',
  'dpid2949',
  'dpid2950',
  'dpid2951',
  'dpid2952',
  'dpid2953',
  'dpid2954',
  'dpid2956',
  'dpid2957',
  'dpid2958',
  'dpid2959',
  'dpid2960',
  'dpid2961',
  'dpid2963',
  'dpid2965',
  'dpid2968',
  'dpid2970',
  'dpid2971',
  'dpid2972',
  'dpid2973',
  'dpid2974',
  'dpid2975',
  'dpid2977',
  'dpid2978',
  'dpid2979',
  'dpid2980',
  'dpid2981',
  'dpid2982',
  'dpid2984',
  'dpid2985',
  'dpid2986',
  'dpid2987',
  'dpid2988',
  'dpid2989',
  'dpid2991',
  'dpid2992',
  'dpid2993',
  'dpid2994',
  'dpid2995',
  'dpid2996',
  'dpid2998',
  'dpid2999',
  'dpid3000',
  'dpid3001',
  'dpid3002',
  'dpid3003',
  'dpid3005',
  'dpid3006',
  'dpid3007',
  'dpid3008',
  'dpid3009',
  'dpid3010',
  'dpid3012',
  'dpid3013',
  'dpid3014',
  'dpid3015',
  'dpid3016',
  'dpid3017',
  'dpid3019',
  'dpid3020',
  'dpid3021',
  'dpid3022',
  'dpid3023',
  'dpid3024',
  'dpid3026',
  'dpid3027',
  'dpid3028',
  'dpid3029',
  'dpid3030',
  'dpid3031',
  'dpid3033',
  'dpid3034',
  'dpid3035',
  'dpid3036',
  'dpid3038',
  'dpid3039',
  'dpid3040',
  'dpid3041',
  'dpid3042',
  'dpid3043',
  'dpid3045',
  'dpid3046',
  'dpid3047',
  'dpid3048',
  'dpid3049',
  'dpid3050',
  'dpid3052',
  'dpid3053',
  'dpid3054',
  'dpid3056',
  'dpid3057',
  'dpid3059',
  'dpid3060',
  'dpid3061',
  'dpid3062',
  'dpid3063',
  'dpid3064',
  'dpid3066',
  'dpid3067',
  'dpid3068',
  'dpid3069',
  'dpid3070',
  'dpid3071',
  'dpid3073',
  'dpid3074',
  'dpid3075',
  'dpid3076',
  'dpid3077',
  'dpid3078',
  'dpid3080',
  'dpid3081',
  'dpid3082',
  'dpid3083',
  'dpid3084',
  'dpid3085',
  'dpid3087',
  'dpid3088',
  'dpid3089',
  'dpid3090',
  'dpid3091',
  'dpid3092',
  'dpid3094',
  'dpid3095',
  'dpid3096',
  'dpid3097',
  'dpid3098',
  'dpid3099',
  'dpid3101',
  'dpid3102',
  'dpid3104',
  'dpid3105',
  'dpid3106',
  'dpid3108',
  'dpid3109',
  'dpid3110',
  'dpid3111',
  'dpid3112',
  'dpid3113',
  'dpid3115',
  'dpid3116',
  'dpid3117',
  'dpid3118',
  'dpid3119',
  'dpid3120',
  'dpid3122',
  'dpid3123',
  'dpid3124',
  'dpid3125',
  'dpid3126',
  'dpid3127',
  'dpid3129',
  'dpid3130',
  'dpid3131',
  'dpid3132',
  'dpid3133',
  'dpid3134',
  'dpid3136',
  'dpid3137',
  'dpid3138',
  'dpid3139',
  'dpid3140',
  'dpid3141',
  'dpid3143',
  'dpid3144',
  'dpid3145',
  'dpid3146',
  'dpid3147',
  'dpid3148',
  'dpid3150',
  'dpid3151',
  'dpid3152',
  'dpid3153',
  'dpid3154',
  'dpid3155',
  'dpid3157',
  'dpid3158',
  'dpid3159',
  'dpid3160',
  'dpid3161',
  'dpid3162',
  'dpid3164',
  'dpid3165',
  'dpid3166',
  'dpid3167',
  'dpid3168',
  'dpid3169',
  'dpid3171',
  'dpid3172',
  'dpid3173',
  'dpid3174',
  'dpid3175',
  'dpid3176',
  'dpid3178',
  'dpid3179',
  'dpid3180',
  'dpid3181',
  'dpid3182',
  'dpid3183',
  'dpid3185',
  'dpid3186',
  'dpid3187',
  'dpid3188',
  'dpid3189',
  'dpid3190',
  'dpid3192',
  'dpid3193',
  'dpid3194',
  'dpid3195',
  'dpid3196',
  'dpid3197',
  'dpid3199',
  'dpid3200',
  'dpid3201',
  'dpid3202',
  'dpid3203',
  'dpid3204',
  'dpid3206',
  'dpid3207',
  'dpid3208',
  'dpid3209',
  'dpid3210',
  'dpid3211',
  'dpid3213',
  'dpid3214',
  'dpid3215',
  'dpid3216',
  'dpid3217',
  'dpid3218',
  'dpid3220',
  'dpid3221',
  'dpid3222',
  'dpid3223',
  'dpid3224',
  'dpid3225',
  'dpid3227',
  'dpid3228',
  'dpid3229',
  'dpid3230',
  'dpid3231',
  'dpid3232',
  'dpid3234',
  'dpid3235',
  'dpid3236',
  'dpid3237',
  'dpid3238',
  'dpid3239',
  'dpid3241',
  'dpid3242',
  'dpid3243',
  'dpid3244',
  'dpid3245',
  'dpid3246',
  'dpid3248',
  'dpid3249',
  'dpid3250',
  'dpid3251',
  'dpid3252',
  'dpid3253',
  'dpid3255',
  'dpid3256',
  'dpid3257',
  'dpid3258',
  'dpid3259',
  'dpid3260',
  'dpid3262',
  'dpid3263',
  'dpid3264',
  'dpid3265',
  'dpid3266',
  'dpid3267',
  'dpid3269',
  'dpid3270',
  'dpid3271',
  'dpid3272',
  'dpid3273',
  'dpid3274',
  'dpid6409',
  'dpid6411',
  'dpid6413',
  'dpid6415',
  'dpid6418',
  'dpid6421',
  'dpid6423',
  'dpid6425',
  'dpid6427',
  'dpid6429',
  'dpid6431',
  'dpid6433',
  'dpid6435',
  'dpid6437',
  'dpid6439',
  'dpid6441',
  'dpid6443',
  'dpid6445',
  'dpid6447',
  'dpid6449',
  'dpid6451',
  'dpid6453',
  'dpid6455',
  'dpid6457',
  'dpid6459',
  'dpid6461',
  'dpid6463',
  'dpid6465',
  'dpid6467',
  'dpid6469',
  'dpid6471',
  'dpid6473',
  'dpid6475',
  'dpid6477',
  'dpid6479',
  'dpid6481',
  'dpid6483',
  'dpid6485',
  'dpid6487',
  'dpid6489',
  'dpid6491',
  'dpid6493',
  'dpid6495',
  'dpid6497',
  'dpid6499',
  'dpid6501',
  'dpid6503',
  'dpid6505',
  'dpid6507',
  'dpid6509',
  'dpid6511',
  'dpid6513',
  'dpid6515',
  'dpid6517',
  'dpid6519',
  'dpid6521',
  'dpid6523',
  'dpid6525',
  'dpid6527',
  'dpid6529',
  'dpid6531',
  'dpid6533',
  'dpid6535',
  'dpid6537',
  'dpid6539',
  'dpid6541',
  'dpid6543',
  'dpid6545',
  'dpid6547',
  'dpid6549',
  'dpid6551',
  'dpid6553',
  'dpid6555',
  'dpid6557',
  'dpid6559',
  'dpid6561',
  'dpid6563',
  'dpid6565',
  'dpid6567',
  'dpid6569',
  'dpid6571',
  'dpid6573',
  'dpid6575',
  'dpid6577',
  'dpid6579',
  'dpid6581',
  'dpid142816',
  'dpid142817',
  'dpid142818',
  'dpid142819',
  'dpid142820',
  'dpid142821',
  'dpid142823',
  'dpid142824',
  'dpid142825',
  'dpid142826',
  'dpid142827',
  'dpid142828',
  'dpid142830',
  'dpid142831',
  'dpid142832',
  'dpid142833',
  'dpid142834',
  'dpid142835',
  'dpid142837',
  'dpid142838',
  'dpid142839',
  'dpid142840',
  'dpid142841',
  'dpid142842',
  'dpid142844',
  'dpid142845',
  'dpid142846',
  'dpid142847',
  'dpid142848',
  'dpid142849',
  'dpid142851',
  'dpid142852',
  'dpid142853',
  'dpid142854',
  'dpid142855',
  'dpid142856',
  'dpid142858',
  'dpid142859',
  'dpid142860',
  'dpid142861',
  'dpid142862',
  'dpid142863',
  'dpid142865',
  'dpid142866',
  'dpid142867',
  'dpid142868',
  'dpid142869',
  'dpid142870',
  'dpid142872',
  'dpid142873',
  'dpid142874',
  'dpid142875',
  'dpid142876',
  'dpid142877',
  'dpid142882',
  'dpid142883',
  'dpid142884',
  'dpid142885',
  'dpid142886',
  'dpid142887',
  'dpid142889',
  'dpid142890',
  'dpid142891',
  'dpid142892',
  'dpid142893',
  'dpid142894',
  'dpid142896',
  'dpid142897',
  'dpid142898',
  'dpid142899',
  'dpid142900',
  'dpid142901',
  'dpid142903',
  'dpid142904',
  'dpid142905',
  'dpid142906',
  'dpid142907',
  'dpid142908',
  'dpid142910',
  'dpid142911',
  'dpid142912',
  'dpid142913',
  'dpid142914',
  'dpid142915',
  'dpid142917',
  'dpid142918',
  'dpid142919',
  'dpid142920',
  'dpid142921',
  'dpid142922',
  'dpid142924',
  'dpid142925',
  'dpid142926',
  'dpid142927',
  'dpid142928',
  'dpid142929',
  'dpid142931',
  'dpid142932',
  'dpid142933',
  'dpid142934',
  'dpid142935',
  'dpid142936',
  'dpid142938',
  'dpid142939',
  'dpid142940',
  'dpid142941',
  'dpid142942',
  'dpid142943',
  'dpid142948',
  'dpid142949',
  'dpid142950',
  'dpid142951',
  'dpid142952',
  'dpid142953',
  'dpid142955',
  'dpid142956',
  'dpid142957',
  'dpid142958',
  'dpid142959',
  'dpid142960',
  'dpid142962',
  'dpid142963',
  'dpid142964',
  'dpid142965',
  'dpid142966',
  'dpid142967',
  'dpid142969',
  'dpid142970',
  'dpid142971',
  'dpid142972',
  'dpid142973',
  'dpid142974',
  'dpid142976',
  'dpid142977',
  'dpid142978',
  'dpid142979',
  'dpid142980',
  'dpid142981',
  'dpid142983',
  'dpid142984',
  'dpid142985',
  'dpid142986',
  'dpid142987',
  'dpid142988',
  'dpid142990',
  'dpid142991',
  'dpid142992',
  'dpid142993',
  'dpid142994',
  'dpid142995',
  'dpid142997',
  'dpid142998',
  'dpid142999',
  'dpid143000',
  'dpid143001',
  'dpid143002',
  'dpid143004',
  'dpid143005',
  'dpid143006',
  'dpid143007',
  'dpid143008',
  'dpid143009',
  'dpid143014',
  'dpid143015',
  'dpid143016',
  'dpid143017',
  'dpid143018',
  'dpid143019',
  'dpid143021',
  'dpid143022',
  'dpid143023',
  'dpid143024',
  'dpid143025',
  'dpid143026',
  'dpid143028',
  'dpid143029',
  'dpid143030',
  'dpid143031',
  'dpid143032',
  'dpid143033',
  'dpid143035',
  'dpid143036',
  'dpid143037',
  'dpid143038',
  'dpid143039',
  'dpid143040',
  'dpid143042',
  'dpid143043',
  'dpid143044',
  'dpid143045',
  'dpid143046',
  'dpid143047',
  'dpid143049',
  'dpid143050',
  'dpid143051',
  'dpid143052',
  'dpid143053',
  'dpid143054',
  'dpid143056',
  'dpid143057',
  'dpid143058',
  'dpid143059',
  'dpid143060',
  'dpid143061',
  'dpid143063',
  'dpid143064',
  'dpid143065',
  'dpid143066',
  'dpid143067',
  'dpid143068',
  'dpid143070',
  'dpid143071',
  'dpid143072',
  'dpid143073',
  'dpid143074',
  'dpid143075',
  'dpid203812',
  'dpid203813',
  'dpid203814',
  'dpid203815',
  'dpid203816',
  'dpid203817',
  'dpid203818',
  'dpid203819',
  'dpid203820',
  'dpid203821',
  'dpid203822',
  'dpid203823',
  'dpid203824',
  'dpid203825',
  'dpid203826',
  'dpid203827',
  'dpid203828',
  'dpid203829',
  'dpid203830',
  'dpid203831',
  'dpid203832',
  'dpid203833',
  'dpid203834',
  'dpid203835',
  'dpid203836',
  'dpid203837',
  'dpid203838',
  'dpid203839',
  'dpid203840',
  'dpid203841',
  'dpid203842',
  'dpid203843',
  'dpid203844',
  'dpid203845',
  'dpid203846',
  'dpid203847',
  'dpid203848',
  'dpid203849',
  'dpid203850',
  'dpid203851',
  'dpid203852',
  'dpid203853',
  'dpid203854',
  'dpid203855',
  'dpid203856',
  'dpid203857',
  'dpid203858',
  'dpid203859',
  'dpid203860',
  'dpid203861',
  'dpid203862',
  'dpid203863',
  'dpid203864',
  'dpid203865',
  'dpid203866',
  'dpid203867',
  'dpid203868',
  'dpid203869',
  'dpid203870',
  'dpid203871',
  'dpid203872',
  'dpid203873',
  'dpid203874',
  'dpid203875',
  'dpid203876',
  'dpid203877',
  'dpid203878',
  'dpid203879',
  'dpid203880',
  'dpid203881',
  'dpid203882',
  'dpid203883',
  'dpid216665',
  'dpid216666',
  'dpid216667',
  'dpid216668',
  'dpid216669',
  'dpid216670',
  'dpid216671',
  'dpid216672',
  'dpid216673',
  'dpid216674',
  'dpid216689',
  'dpid216701',
  'dpid216707']

table_autoencoderData = db_tables.autoencoderData(dpids=dpid_colnames)