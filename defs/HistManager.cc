#include "HistManager.h"

  HistManager::HistManager(TFile* myFile){
    theFile =  myFile;
  }


  HistManager::~HistManager(){

  }
    
    
  void HistManager::writeHists(TFile* theFile){
    
    theFile->cd();
    std::map<std::string,TH1F*>::const_iterator mapit1;
    std::map<std::string,TH2F*>::const_iterator mapit2;
    std::map<std::string,TProfile*>::const_iterator mapit3;
    for (mapit1 = the1DMap.begin(); mapit1 != the1DMap.end(); ++mapit1){
      (*mapit1).second->Write();
    }
    for (mapit2 = the2DMap.begin(); mapit2 != the2DMap.end(); ++mapit2){
      (*mapit2).second->Write();
    }
    for (mapit3 = theProfMap.begin(); mapit3 != theProfMap.end(); ++mapit3){
      (*mapit3).second->Write();
    }
    theFile->cd();
    theFile->Close();
    
  }
    

  void HistManager::fill1DHist(float x, std::string name, std::string title,
                               int bins, float xmin, float xmax, float weight, std::string folder){
  
    std::map<std::string,TH1F*>::iterator it;
    std::string name1(name.c_str());
    it = the1DMap.find(name1);
    if (it == the1DMap.end()){
      theFile->cd(folder.c_str());
      the1DMap[name1] = new TH1F(name.c_str(),title.c_str(),bins,xmin,xmax);
      the1DMap[name1]->Sumw2();
      theFile->cd();
    }

    the1DMap[name1]->Fill(x,weight);

  }

  void HistManager::fill1DHistUnevenBins(float x, std::string name, std::string title,
                                         int bins, float *binEdges, float weight, std::string folder){
    std::map<std::string,TH1F*>::iterator it;
    std::string name1(name.c_str());
    it = the1DMap.find(name1);
    if (it == the1DMap.end()){
      theFile->cd(folder.c_str());
      the1DMap[name1] = new TH1F(name.c_str(),title.c_str(),bins,binEdges);
      the1DMap[name1]->Sumw2();
      theFile->cd();
    }


    the1DMap[name1]->Fill(x,weight);

  }




  void HistManager::fill2DHist(float x, float y,std::string name, std::string title,
                               int binsx, float xmin, float xmax,
                               int binsy, float ymin, float ymax, float weight, std::string folder){

    std::map<std::string,TH2F*>::iterator it;
    std::string name1(name.c_str());
    it = the2DMap.find(name1);
    if (it == the2DMap.end()){
      theFile->cd(folder.c_str());
      the2DMap[name1] = new TH2F(name.c_str(),title.c_str(),binsx,xmin,xmax,binsy,ymin,ymax);
      the2DMap[name1]->Sumw2();
      theFile->cd();
    }

    the2DMap[name1]->Fill(x,y,weight);

  }

  void HistManager::fill2DHistUnevenBins(float x, float y, std::string name, std::string title,
                                         int binsx, float *binEdgesx,
                                         int binsy, float *binEdgesy, float weight,  std::string folder){

    std::map<std::string,TH2F*>::iterator it;
    std::string name1(name.c_str());
    it = the2DMap.find(name1);
    if (it == the2DMap.end()){
      theFile->cd(folder.c_str());
      the2DMap[name1] = new TH2F(name.c_str(),title.c_str(),binsx,binEdgesx,binsy,binEdgesy);
      the2DMap[name1]->Sumw2();
      theFile->cd();
    }


    the2DMap[name1]->Fill(x,y,weight);
  }


  void HistManager::fill3DHistUnevenBins(float x, float y, float z, std::string name, std::string title,
                                         int binsx, float *binEdgesx,
                                         int binsy, float *binEdgesy, 
                                         int binsz, float *binEdgesz,
                                         float weight,  std::string folder){

    std::map<std::string,TH3F*>::iterator it;
    std::string name1(name.c_str());
    it = the3DMap.find(name1);
    if (it == the3DMap.end()){
      theFile->cd(folder.c_str());
      the3DMap[name1] = new TH3F(name.c_str(),title.c_str(),binsx,binEdgesx,binsy,binEdgesy,binsz,binEdgesz);
      the3DMap[name1]->Sumw2();
      theFile->cd();
    }


    the3DMap[name1]->Fill(x,y,z,weight);
  }


  void HistManager::fillProfile(float x, float y, std::string name, std::string title,
                                int binsx, float xmin, float xmax,
                                float ymin, float ymax, float weight,  std::string folder){

    std::map<std::string,TProfile*>::iterator it;
    std::string name1(name.c_str());
    it = theProfMap.find(name1);
    if (it == theProfMap.end()){
      theFile->cd(folder.c_str());
      theProfMap[name1] = new TProfile(name.c_str(),title.c_str(),binsx,xmin,xmax,ymin,ymax);
      theProfMap[name1]->Sumw2();
      theFile->cd();
    }

    theProfMap[name1]->Fill(x,y,weight);

  }


