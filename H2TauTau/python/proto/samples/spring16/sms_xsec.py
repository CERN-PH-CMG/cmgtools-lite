
xsec_vs_m_slepton = {
    50:943.29,
    100:102.77,
    150:25.53 ,
    200:9.,
    250:3.85,
    300:1.87,
    350:0.99,
    400:0.56,
    450:0.33,
    500:0.2,
}

def get_xsec(m_slepton=50):
    '''returns cross section in pb as function of slepton mass'''
    if m_slepton in xsec_vs_m_slepton:
        return xsec_vs_m_slepton[m_slepton]/1000.
    
    print 'Trying to get cross section but slepton mass', m_slepton, 'not in dict and not interpolating just yet'
    return 1.

    #if m_slepton < min(xsec_vs_m_slepton.keys()) or m_slepton > m
