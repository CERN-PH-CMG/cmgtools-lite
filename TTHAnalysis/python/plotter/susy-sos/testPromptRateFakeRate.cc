#include <iostream> 
#include "../fakeRate.cc"

void runTest(const char *test, float FR1, float PR1, float FR2, float PR2) 
{
    std::cout << "Test: " << test << std::endl;
    FRi_mu[2]->SetBinContent(1,1, FR1);
    FRi_mu[3]->SetBinContent(1,1, PR1);
    FRi_el[2]->SetBinContent(1,1, FR2);
    FRi_el[3]->SetBinContent(1,1, PR2);
    std::cout << "   Lepton 1: Fake rate: " << FR1 << ", Prompt rate: " << PR1 << std::endl;
    std::cout << "   Lepton 2: Fake rate: " << FR2 << ", Prompt rate: " << PR2 << std::endl;

    std::cout << "Inclusive prediction: " << std::endl;
    std::cout << "   Weight for TT -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  1, 20.,1.,11,  1,  2,3,  -1,  11) << std::endl;
    std::cout << "   Weight for TL -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  1, 20.,1.,11,  0,  2,3,  -1,  11) << std::endl;
    std::cout << "   Weight for LT -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  0, 20.,1.,11,  1,  2,3,  -1,  11) << std::endl;
    std::cout << "   Weight for LL -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  0, 20.,1.,11,  0,  2,3,  -1,  11) << std::endl;
    std::cout << "Single fakes only: " << std::endl;
    std::cout << "   Weight for TT -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  1, 20.,1.,11,  1,  2,3,  1,  11)+fakeRatePromptRateWeight_2l_ij(20.,1.,13,  1, 20.,1.,11,  1,  2,3,  10,  11) << std::endl;
    std::cout << "   Weight for TL -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  1, 20.,1.,11,  0,  2,3,  1,  11)+fakeRatePromptRateWeight_2l_ij(20.,1.,13,  1, 20.,1.,11,  0,  2,3,  10,  11) << std::endl;
    std::cout << "   Weight for LT -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  0, 20.,1.,11,  1,  2,3,  1,  11)+fakeRatePromptRateWeight_2l_ij(20.,1.,13,  0, 20.,1.,11,  1,  2,3,  10,  11) << std::endl;
    std::cout << "   Weight for LL -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  0, 20.,1.,11,  0,  2,3,  1,  11)+fakeRatePromptRateWeight_2l_ij(20.,1.,13,  0, 20.,1.,11,  0,  2,3,  10,  11) << std::endl;
    std::cout << "Double fakes only: " << std::endl;
    std::cout << "   Weight for TT -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  1, 20.,1.,11,  1,  2,3,  0,  11) << std::endl;
    std::cout << "   Weight for TL -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  1, 20.,1.,11,  0,  2,3,  0,  11) << std::endl;
    std::cout << "   Weight for LT -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  0, 20.,1.,11,  1,  2,3,  0,  11) << std::endl;
    std::cout << "   Weight for LL -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  0, 20.,1.,11,  0,  2,3,  0,  11) << std::endl;
    std::cout << "Full transfer matrix: " << std::endl;
    std::cout << "   Weight for TT -> PP -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  1, 20.,1.,11,  1,  2,3,  11,  11) << std::endl;
    std::cout << "   Weight for TL -> PP -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  1, 20.,1.,11,  0,  2,3,  11,  11) << std::endl;
    std::cout << "   Weight for LT -> PP -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  0, 20.,1.,11,  1,  2,3,  11,  11) << std::endl;
    std::cout << "   Weight for LL -> PP -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  0, 20.,1.,11,  0,  2,3,  11,  11) << std::endl;
    std::cout << "   ------------------ " << std::endl;
    std::cout << "   Weight for TT -> PF -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  1, 20.,1.,11,  1,  2,3,  10,  11) << std::endl;
    std::cout << "   Weight for TL -> PF -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  1, 20.,1.,11,  0,  2,3,  10,  11) << std::endl;
    std::cout << "   Weight for LT -> PF -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  0, 20.,1.,11,  1,  2,3,  10,  11) << std::endl;
    std::cout << "   Weight for LL -> PF -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  0, 20.,1.,11,  0,  2,3,  10,  11) << std::endl;
    std::cout << "   ------------------ " << std::endl;
    std::cout << "   Weight for TT -> FP -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  1, 20.,1.,11,  1,  2,3,   1,  11) << std::endl;
    std::cout << "   Weight for TL -> FP -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  1, 20.,1.,11,  0,  2,3,   1,  11) << std::endl;
    std::cout << "   Weight for LT -> FP -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  0, 20.,1.,11,  1,  2,3,   1,  11) << std::endl;
    std::cout << "   Weight for LL -> FP -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  0, 20.,1.,11,  0,  2,3,   1,  11) << std::endl;
    std::cout << "   ------------------ " << std::endl;
    std::cout << "   Weight for TT -> FF -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  1, 20.,1.,11,  1,  2,3,   0,  11) << std::endl;
    std::cout << "   Weight for TL -> FF -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  1, 20.,1.,11,  0,  2,3,   0,  11) << std::endl;
    std::cout << "   Weight for LT -> FF -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  0, 20.,1.,11,  1,  2,3,   0,  11) << std::endl;
    std::cout << "   Weight for LL -> FF -> SR: " << fakeRatePromptRateWeight_2l_ij(20.,1.,13,  0, 20.,1.,11,  0,  2,3,   0,  11) << std::endl;

    std::cout << "\n" << std::endl;
}

void testPromptRateFakeRate() {
    TH2F hPR("PR","PR",1,0,100,1,0,2.5);
    TH2F hFR("FR","FR",1,0,100,1,0,2.5);
    TH2F hPR2("PR2","PR2",1,0,100,1,0,2.5);
    TH2F hFR2("FR2","FR2",1,0,100,1,0,2.5);
    FRi_mu[2] = & hFR;
    FRi_el[2] = & hFR2;
    FRi_mu[3] = & hPR;
    FRi_el[3] = & hPR2;
    
    runTest("Trivial", 0.1, 1, 0.2, 1);
    runTest("Easy",    0.1, 0.99, 0.2, 0.99);
    runTest("Real",    0.1, 0.6, 0.2, 0.9);
}
