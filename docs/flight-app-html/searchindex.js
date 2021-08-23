Search.setIndex({docnames:["index"],envversion:{"sphinx.domains.c":1,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":1,"sphinx.domains.javascript":1,"sphinx.domains.math":2,"sphinx.domains.python":1,"sphinx.domains.rst":1,"sphinx.domains.std":1,"sphinx.ext.todo":2,"sphinx.ext.viewcode":1,sphinx:56},filenames:["index.rst"],objects:{"src.Controllers":{Exceptions:[0,0,0,"-"],OpenCVThreadedController:[0,0,0,"-"],PhoneController:[0,0,0,"-"],Program_Controller:[0,0,0,"-"]},"src.Controllers.Exceptions":{FailedDisconnectException:[0,1,1,""],FailedRPIFlashException:[0,1,1,""],PhonesNotSyncedException:[0,1,1,""],RPINotConnectedException:[0,1,1,""],RecordingNotStartedException:[0,1,1,""],TransferNotStartedException:[0,1,1,""],VideoCorruptedException:[0,1,1,""],VideoNotPresentException:[0,1,1,""]},"src.Controllers.OpenCVThreadedController":{DroneTracker:[0,2,1,""],VideoCorruptedException:[0,1,1,""],VideoNotPresentException:[0,1,1,""],compute_coordinates:[0,4,1,""],get_phone_id:[0,4,1,""],main:[0,4,1,""],merge_data_points:[0,4,1,""]},"src.Controllers.OpenCVThreadedController.DroneTracker":{is_light_on:[0,3,1,""],read_video:[0,3,1,""],rescale_frame:[0,3,1,""],resize_bbox:[0,3,1,""],trackDrone:[0,3,1,""]},"src.Controllers.PhoneController":{PhoneControl:[0,2,1,""]},"src.Controllers.PhoneController.PhoneControl":{closeConn:[0,3,1,""],isTransferring:[0,3,1,""],setupSocket:[0,3,1,""],startFileTransfer:[0,3,1,""],startRecording:[0,3,1,""],stopRecording:[0,3,1,""],sync:[0,3,1,""],synced:[0,3,1,""],threadSendSignal:[0,3,1,""],threadWaitForFileTransfer:[0,3,1,""],waitForFileTransfer:[0,3,1,""]},"src.Controllers.Program_Controller":{Controller:[0,2,1,""],close_conn:[0,4,1,""],createPhoneConnection:[0,4,1,""],main:[0,4,1,""]},"src.Controllers.Program_Controller.Controller":{cleanup:[0,3,1,""],get_all_files:[0,3,1,""],get_flight_info:[0,3,1,""],get_in_order:[0,3,1,""],import_flight:[0,3,1,""],setupFileStructure:[0,3,1,""],show_home:[0,3,1,""],show_loading_window:[0,3,1,""],show_report_window:[0,3,1,""],show_tracking_window:[0,3,1,""],show_verify_screen:[0,3,1,""],start_analysis:[0,3,1,""],transfer_complete:[0,3,1,""],transfer_footage:[0,3,1,""],updateFlightStatus:[0,3,1,""],wait_for_analysis:[0,3,1,""]},"src.Export":{ExportFile:[0,0,0,"-"],ImportFile:[0,0,0,"-"]},"src.Export.ExportFile":{export_data:[0,4,1,""]},"src.Export.ImportFile":{importData:[0,4,1,""]},"src.Tests":{Graph_Test:[0,0,0,"-"],ImportFile_Test:[0,0,0,"-"]},"src.Tests.Graph_Test":{Graph_Test:[0,2,1,""]},"src.Tests.Graph_Test.Graph_Test":{test_checkLegalInput:[0,3,1,""],test_computeVelocity:[0,3,1,""],test_graphShows_noError:[0,3,1,""],test_readCoordinates_size100_allLegal:[0,3,1,""],test_readCoordinates_size100_someLegal:[0,3,1,""],test_readCoordinates_size1200_allLegal:[0,3,1,""],test_readCoordinates_size1200_someLegal:[0,3,1,""],test_readCoordinates_size200_allLegal:[0,3,1,""],test_readCoordinates_size200_someLegal:[0,3,1,""],test_readCoordinates_size600_allLegal:[0,3,1,""],test_readCoordinates_size600_someLegal:[0,3,1,""],test_readCoordinates_small_illegal:[0,3,1,""],test_readCoordinates_small_legal:[0,3,1,""],test_smoothnessComputes:[0,3,1,""],test_smoothnessValues:[0,3,1,""],test_velocityColors:[0,3,1,""],test_velocityColorsComputes_correctSize:[0,3,1,""],test_velocityComputes_correctSize:[0,3,1,""],test_velocityPoints:[0,3,1,""]},"src.Tests.ImportFile_Test":{ImportFileTests:[0,2,1,""]},"src.Tests.ImportFile_Test.ImportFileTests":{test_import:[0,3,1,""]},"src.Views":{Graph:[0,0,0,"-"],View_LoadingScreen:[0,0,0,"-"],View_ReportScreen:[0,0,0,"-"],View_StartupScreen:[0,0,0,"-"],View_TrackingScreen:[0,0,0,"-"],View_VerifySetupScreen:[0,0,0,"-"]},"src.Views.Graph":{checkCoordinates:[0,4,1,""],checkLegalInput:[0,4,1,""],computeVelocity:[0,4,1,""],computeVelocityStatistics:[0,4,1,""],dimensionless_jerk:[0,4,1,""],generateGraph:[0,4,1,""],log_dimensionless_jerk:[0,4,1,""],velocityColors:[0,4,1,""],velocityPoints:[0,4,1,""]},"src.Views.View_LoadingScreen":{LoadingWindow:[0,2,1,""]},"src.Views.View_LoadingScreen.LoadingWindow":{BtnHome:[0,3,1,""],BtnTestReport:[0,3,1,""],LblStatus:[0,3,1,""],del_BtnHome:[0,3,1,""],del_BtnTestReport:[0,3,1,""],del_LblStatus:[0,3,1,""],initView:[0,3,1,""],returnHome:[0,3,1,""],setSubtitle:[0,3,1,""],setTitle:[0,3,1,""],set_BtnHome:[0,3,1,""],set_BtnTestReport:[0,3,1,""],set_LblStatus:[0,3,1,""],setupLoadingIcon:[0,3,1,""],signalTestReport:[0,3,1,""],signalTransferFootage:[0,3,1,""]},"src.Views.View_ReportScreen":{ReportWindow:[0,2,1,""]},"src.Views.View_ReportScreen.ReportWindow":{BtnExport:[0,3,1,""],BtnFlyAgain:[0,3,1,""],BtnHome:[0,3,1,""],BtnViewGraphNoVelocity:[0,3,1,""],BtnViewGraphVelocity:[0,3,1,""],LblFlightDate:[0,3,1,""],LblFlightInstructions:[0,3,1,""],LblFlightLength:[0,3,1,""],LblInstructor:[0,3,1,""],LblPilot:[0,3,1,""],analyzeFlight:[0,3,1,""],createStatisticsTable:[0,3,1,""],del_BtnExport:[0,3,1,""],del_BtnFlyAgain:[0,3,1,""],del_BtnHome:[0,3,1,""],del_BtnViewGraphNoVelocity:[0,3,1,""],del_BtnViewGraphVelocity:[0,3,1,""],del_LblFlightDate:[0,3,1,""],del_LblFlightInstructions:[0,3,1,""],del_LblFlightLength:[0,3,1,""],del_LblInstructor:[0,3,1,""],del_LblPilot:[0,3,1,""],handleEndSliderValueChange:[0,3,1,""],handleStartSliderValueChange:[0,3,1,""],initView:[0,3,1,""],setButtonLayout:[0,3,1,""],setSubTitle:[0,3,1,""],set_BtnExport:[0,3,1,""],set_BtnFlyAgain:[0,3,1,""],set_BtnHome:[0,3,1,""],set_BtnViewGraphNoVelocity:[0,3,1,""],set_BtnViewGraphVelocity:[0,3,1,""],set_LblFlightDate:[0,3,1,""],set_LblFlightInstructions:[0,3,1,""],set_LblFlightLength:[0,3,1,""],set_LblInstructor:[0,3,1,""],set_LblPilot:[0,3,1,""],setupFlightInfo:[0,3,1,""],setupGraph:[0,3,1,""],setupSlider:[0,3,1,""],setupTitle:[0,3,1,""],showWindow:[0,3,1,""],signalExportResults:[0,3,1,""],signalReturnHome:[0,3,1,""],signalStartTracking:[0,3,1,""]},"src.Views.View_StartupScreen":{StartupWindow:[0,2,1,""]},"src.Views.View_StartupScreen.StartupWindow":{BtnImport:[0,3,1,""],BtnStart:[0,3,1,""],BtnVerifySetup:[0,3,1,""],del_BtnImport:[0,3,1,""],del_BtnStart:[0,3,1,""],del_BtnVerifySetup:[0,3,1,""],initView:[0,3,1,""],openFileNameDialog:[0,3,1,""],setButtonLayout:[0,3,1,""],setTeamMembers:[0,3,1,""],setTitle:[0,3,1,""],set_BtnImport:[0,3,1,""],set_BtnStart:[0,3,1,""],set_BtnVerifySetup:[0,3,1,""],setupAMLogo:[0,3,1,""],setupPicture:[0,3,1,""],signalImportFlight:[0,3,1,""],signalStartTracking:[0,3,1,""],signalVerifySetup:[0,3,1,""]},"src.Views.View_TrackingScreen":{TrackingWindow:[0,2,1,""]},"src.Views.View_TrackingScreen.TrackingWindow":{BtnClear:[0,3,1,""],BtnConfirm:[0,3,1,""],BtnStart:[0,3,1,""],BtnStop:[0,3,1,""],LblInstructor:[0,3,1,""],LblPilot:[0,3,1,""],LblTimer:[0,3,1,""],TBInstructor:[0,3,1,""],TBPilot:[0,3,1,""],TEInstructions:[0,3,1,""],clearValues:[0,3,1,""],confirmValues:[0,3,1,""],del_BtnClear:[0,3,1,""],del_BtnConfirm:[0,3,1,""],del_BtnStart:[0,3,1,""],del_BtnStop:[0,3,1,""],del_LblInstructor:[0,3,1,""],del_LblPilot:[0,3,1,""],del_LblTimer:[0,3,1,""],del_TBInstructor:[0,3,1,""],del_TBPilot:[0,3,1,""],del_TEInstructions:[0,3,1,""],initView:[0,3,1,""],returnHome:[0,3,1,""],setClrConfirmBtns:[0,3,1,""],setFlightInstructions:[0,3,1,""],setInstructor:[0,3,1,""],setPilot:[0,3,1,""],setStartAndStopBtns:[0,3,1,""],setStatusLabel:[0,3,1,""],setSubTitle:[0,3,1,""],setTimerLabel:[0,3,1,""],setTitle:[0,3,1,""],set_BtnClear:[0,3,1,""],set_BtnConfirm:[0,3,1,""],set_BtnStart:[0,3,1,""],set_BtnStop:[0,3,1,""],set_LblInstructor:[0,3,1,""],set_LblPilot:[0,3,1,""],set_LblTimer:[0,3,1,""],set_TBInstructor:[0,3,1,""],set_TBPilot:[0,3,1,""],set_TEInstructions:[0,3,1,""],startTracking:[0,3,1,""],stopTracking:[0,3,1,""]},"src.Views.View_VerifySetupScreen":{VerifySetupWindow:[0,2,1,""]},"src.Views.View_VerifySetupScreen.VerifySetupWindow":{BtnCheck:[0,3,1,""],BtnHome:[0,3,1,""],BtnPhoneSync:[0,3,1,""],BtnTestFull:[0,3,1,""],BtnTestLight:[0,3,1,""],checkStatus:[0,3,1,""],del_BtnCheck:[0,3,1,""],del_BtnHome:[0,3,1,""],del_BtnPhoneSync:[0,3,1,""],del_BtnTestFull:[0,3,1,""],del_BtnTestLight:[0,3,1,""],initView:[0,3,1,""],returnHome:[0,3,1,""],setButtonLayout:[0,3,1,""],setTitle:[0,3,1,""],set_BtnCheck:[0,3,1,""],set_BtnHome:[0,3,1,""],set_BtnPhoneSync:[0,3,1,""],set_BtnTestFull:[0,3,1,""],set_BtnTestLight:[0,3,1,""],setupPicture:[0,3,1,""],syncPhone:[0,3,1,""],testFull:[0,3,1,""],testLight:[0,3,1,""]}},objnames:{"0":["py","module","Python module"],"1":["py","exception","Python exception"],"2":["py","class","Python class"],"3":["py","method","Python method"],"4":["py","function","Python function"]},objtypes:{"0":"py:module","1":"py:exception","2":"py:class","3":"py:method","4":"py:function"},terms:{"1080p":0,"boolean":0,"class":0,"float":0,"function":0,"int":0,"new":0,"return":0,"switch":0,"true":0,"try":0,FOR:0,For:0,One:0,The:0,USED:0,Use:0,Used:0,Will:0,__btncheck:0,__btnclear:0,__btnconfirm:0,__btnexport:0,__btnflyagain:0,__btnhome:0,__btnimport:0,__btnphonesync:0,__btnstart:0,__btnstop:0,__btntestful:0,__btntestlight:0,__btnverifysetup:0,__btnviewgraphnoveloc:0,__btnviewgraphveloc:0,__btnviewinstruct:0,abl:0,access:0,action:0,activ:0,actual:0,adjust:0,after:0,again:0,alert:0,all:0,allow:0,alongsid:0,alreadi:0,also:0,analysi:0,analyz:0,analyzeflight:0,ani:0,anim:0,anoth:0,anyth:0,app:0,applic:0,argument:0,around:0,arrai:0,assign:0,attach:0,axi:0,back:0,base:0,bbox:0,been:0,befor:0,begin:0,being:0,below:0,between:0,blank:0,bool:0,both:0,bottom:0,bound:0,box:0,box_height:0,box_width:0,btncheck:0,btnclear:0,btnconfirm:0,btnexport:0,btnflyagain:0,btnhome:0,btnimport:0,btnphonesync:0,btnstart:0,btnstop:0,btntestful:0,btntestlight:0,btntestreport:0,btnverifysetup:0,btnviewgraphnoveloc:0,btnviewgraphveloc:0,bug:0,button:0,calcul:0,call:0,camera:0,can:0,cancel:0,cannot:0,cell:0,chang:0,check:0,checkcoordin:0,checklegalinput:0,checkstatu:0,child:0,chosen:0,cleanup:0,clear:0,clearvalu:0,click:0,close:0,close_conn:0,closeconn:0,code:0,color:0,commmun:0,commun:0,complet:0,compon:0,comput:0,compute_coordin:0,computeveloc:0,computevelocitystatist:0,config:0,configur:0,confirm:0,confirmvalu:0,conn:0,connect:0,consecut:0,contain:0,continu:0,coordin:0,correct:0,correctli:0,corrupt:0,count:0,creat:0,createphoneconnect:0,createstatisticst:0,data:0,datapoint:0,date:0,del_btncheck:0,del_btnclear:0,del_btnconfirm:0,del_btnexport:0,del_btnflyagain:0,del_btnhom:0,del_btnimport:0,del_btnphonesync:0,del_btnstart:0,del_btnstop:0,del_btntestful:0,del_btntestlight:0,del_btntestreport:0,del_btnverifysetup:0,del_btnviewgraphnoveloc:0,del_btnviewgraphveloc:0,del_lblflightd:0,del_lblflightinstruct:0,del_lblflightlength:0,del_lblinstructor:0,del_lblpilot:0,del_lblstatu:0,del_lbltim:0,del_tbinstructor:0,del_tbpilot:0,del_teinstruct:0,delet:0,denot:0,depend:0,detect:0,determin:0,dialog:0,dict:0,dictionari:0,did:0,differ:0,dimension:0,dimensionless:0,dimensionless_jerk:0,directori:0,disconnect:0,displai:0,displayveloc:0,doesn:0,doing:0,don:0,donald:0,done:0,draw:0,drawn:0,driver:0,dronecontrol:0,dronetrack:0,dure:0,each:0,easier:0,eckert:0,edit:0,element:0,elrod:0,empti:0,end:0,enough:0,ensur:0,enter:0,entir:0,error:0,essenti:0,estim:0,everi:0,exampl:0,execut:0,exist:0,exit:0,expect:0,export_data:0,exportfil:0,extens:0,extra:0,extract:0,factor:0,fail:0,faileddisconnectexcept:0,failedrpiflashexcept:0,fals:0,field:0,figur:0,filenam:0,filepath:0,finish:0,first:0,flag:0,flash:0,flightdat:0,flightdata:0,flightdict:0,flightinstruct:0,flightlength:0,flightmodeen:0,flightpath:0,fly:0,folder:0,folderpath:0,follow:0,footag:0,format:0,frame:0,frequenc:0,from:0,ftp:0,full:0,gener:0,generategraph:0,get:0,get_all_fil:0,get_flight_info:0,get_in_ord:0,get_phone_id:0,getter:0,gif:0,given:0,goe:0,going:0,grab:0,graph_test:0,greater:0,green:0,grid:0,had:0,hand:0,handleendslidervaluechang:0,handlestartslidervaluechang:0,has:0,have:0,haylei:0,here:0,home:0,horizont:0,icon:0,illeg:0,imag:0,import_flight:0,importdata:0,importfil:0,importfile_test:0,importfiletest:0,improv:0,includ:0,incom:0,incorrect:0,index:0,info:0,inform:0,initi:0,initview:0,inpath:0,input:0,instruct:0,instructor:0,instructornam:0,intend:0,interact:0,interfac:0,intuit:0,is_light_on:0,ismael:0,issu:0,istransf:0,its:0,jerk:0,jonathan:0,json:0,just:0,keep:0,kei:0,know:0,label:0,lai:0,laptop:0,later:0,layout:0,lblflightdat:0,lblflightinstruct:0,lblflightlength:0,lblinstructor:0,lblpilot:0,lblstatu:0,lbltimer:0,least:0,left:0,legal:0,legalpoint:0,length:0,less:0,let:0,lifecycl:0,light:0,line:0,list:0,listen:0,loadingwindow:0,lock:0,log:0,log_dimensionless_jerk:0,logo:0,loop:0,main:0,make:0,match:0,matplotlib:0,maximum:0,mean:0,measur:0,member:0,merg:0,merge_data_point:0,messag:0,method:0,methodnam:0,metric:0,minimum:0,modifi:0,modul:0,more:0,move:0,movement:0,mp4:0,much:0,must:0,name:0,need:0,network:0,none:0,note:0,number:0,numpi:0,object:0,onc:0,one:0,onli:0,onto:0,open:0,opencvcontrol:0,opencvthreadedcontrol:0,openfilenamedialog:0,oper:0,option:0,order:0,origin:0,other:0,otherwis:0,our:0,out:0,outpath:0,output:0,outsid:0,over:0,page:0,panel:0,parallel:0,param:0,paramet:0,pass:0,past:0,path:0,percent:0,percentag:0,perform:0,phone1point:0,phone2point:0,phone:0,phonesnotsyncedexcept:0,phonesync:0,pilot:0,pilotnam:0,pixel:0,plot:0,point:0,pop:0,popul:0,port:0,portno:0,portnum:0,posit:0,press:0,prevent:0,previou:0,previousflight:0,procedur:0,process:0,profil:0,program_control:0,project:0,properti:0,purpos:0,push:0,put:0,pyqt5:0,qgridlayout:0,qhboxlayout:0,qlabel:0,qmovi:0,qtablewidget:0,qtimer:0,qtwidget:0,qvboxlayout:0,rais:0,ran:0,raspberri:0,raw:0,read:0,read_video:0,real:0,receiv:0,record:0,recordingnotstartedexcept:0,red:0,refer:0,reli:0,reload:0,reportwindow:0,repres:0,requir:0,rescal:0,rescale_fram:0,resiz:0,resize_bbox:0,respect:0,respons:0,result:0,returnhom:0,rewrit:0,rodriguez:0,roll:0,rpi:0,rpinotconnectedexcept:0,run:0,runtest:0,sai:0,same:0,sampl:0,save:0,scale:0,score:0,search:0,second:0,section:0,see:0,segment:0,select:0,send:0,separ:0,session:0,set:0,set_btncheck:0,set_btnclear:0,set_btnconfirm:0,set_btnexport:0,set_btnflyagain:0,set_btnhom:0,set_btnimport:0,set_btnphonesync:0,set_btnstart:0,set_btnstop:0,set_btntestful:0,set_btntestlight:0,set_btntestreport:0,set_btnverifysetup:0,set_btnviewgraphnoveloc:0,set_btnviewgraphveloc:0,set_lblflightd:0,set_lblflightinstruct:0,set_lblflightlength:0,set_lblinstructor:0,set_lblpilot:0,set_lblstatu:0,set_lbltim:0,set_tbinstructor:0,set_tbpilot:0,set_teinstruct:0,setbuttonlayout:0,setclrconfirmbtn:0,setflightinstruct:0,setinstructor:0,setpilot:0,setstartandstopbtn:0,setstatuslabel:0,setsubtitl:0,setteammemb:0,settimerlabel:0,settitl:0,setupamlogo:0,setupfilestructur:0,setupflightinfo:0,setupgraph:0,setuploadingicon:0,setuppictur:0,setupslid:0,setupsocket:0,setuptitl:0,should:0,show:0,show_hom:0,show_loading_window:0,show_report_window:0,show_tracking_window:0,show_verify_screen:0,shown:0,showwindow:0,shrunk:0,sigack:0,sigmessag:0,signal:0,signalexportresult:0,signalimportflight:0,signalreturnhom:0,signalstarttrack:0,signaltestreport:0,signaltransferfootag:0,signalverifysetup:0,simpl:0,singl:0,size:0,slider:0,slower:0,small:0,smartphon:0,smooth:0,socket:0,someth:0,sourc:0,spawn:0,specif:0,specifi:0,speed:0,splice:0,src:0,start:0,start_acknowledg:0,start_analysi:0,start_ftp:0,start_ftp_acknowledg:0,startfiletransf:0,startrecord:0,starttrack:0,startupwindow:0,statist:0,statu:0,still:0,stop:0,stop_acknowledg:0,stoprecord:0,stoptrack:0,store:0,str:0,string:0,structur:0,suass:0,sub:0,subtitl:0,successfulli:0,sure:0,sync:0,syncphon:0,system:0,take:0,taken:0,tbinstructor:0,tbpilot:0,tcp:0,team:0,teinstruct:0,tell:0,test_checklegalinput:0,test_computeveloc:0,test_graphshows_noerror:0,test_import:0,test_readcoordinates_size100_allleg:0,test_readcoordinates_size100_someleg:0,test_readcoordinates_size1200_allleg:0,test_readcoordinates_size1200_someleg:0,test_readcoordinates_size200_allleg:0,test_readcoordinates_size200_someleg:0,test_readcoordinates_size600_allleg:0,test_readcoordinates_size600_someleg:0,test_readcoordinates_small_illeg:0,test_readcoordinates_small_leg:0,test_smoothnesscomput:0,test_smoothnessvalu:0,test_velocitycolor:0,test_velocitycolorscomputes_corrects:0,test_velocitycomputes_corrects:0,test_velocitypoint:0,testful:0,testlight:0,text:0,textbox:0,than:0,thei:0,them:0,thi:0,those:0,though:0,thread:0,threadsendsign:0,threadwaitforfiletransf:0,through:0,time:0,timediff:0,timer:0,titl:0,togeth:0,top:0,trackdron:0,trackingwindow:0,transfer:0,transfer_complet:0,transfer_footag:0,transfernotstartedexcept:0,translat:0,tri:0,tupl:0,turn:0,two:0,type:0,until:0,updat:0,updateflightstatu:0,upon:0,use:0,used:0,user:0,uses:0,using:0,usingpreviousflight:0,valid:0,valu:0,variabl:0,veloc:0,velocitycolor:0,velocitypoint:0,velocityvalu:0,verif:0,verifysetup:0,verifysetupwindow:0,version:0,vertic:0,video:0,videocorruptedexcept:0,videofil:0,videonotpresentexcept:0,view:0,view_loadingscreen:0,view_reportscreen:0,view_startupscreen:0,view_trackingscreen:0,view_verifysetupscreen:0,visual:0,wait:0,wait_for_analysi:0,waitforfiletransf:0,want:0,went:0,were:0,westerfield:0,what:0,when:0,which:0,who:0,window:0,within:0,without:0,work:0,world:0,written:0,wrong:0,x_coord:0,xcoordin:0,y_coord:0,ycoordin:0,yellow:0,z_coord:0,zcoordin:0},titles:["Welcome to Drone Tracker\u2019s documentation!"],titleterms:{"export":0,"import":0,control:0,document:0,drone:0,except:0,file:0,flight:0,graph:0,indic:0,intro:0,load:0,matplot:0,opencv:0,phonecontrol:0,program:0,report:0,screen:0,setup:0,startup:0,tabl:0,test:0,track:0,tracker:0,verifi:0,welcom:0}})