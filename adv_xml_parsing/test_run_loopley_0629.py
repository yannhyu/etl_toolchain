# test_run_loopley_0629.py
import os
import glob
import xmltodict
#import json
from iso_toolchain import write, scrub_data_value
from evendict import flush

def digest_iso_resp(filename):
    iso_results = []
    with open(filename, 'r') as fh:
        xml = fh.read().replace('\n', '')
        res = xmltodict.parse(xml)
        #print(json.dumps(result, indent=4))
        inflated_res = flush(res)
        case_of_no_match = False
        for k, v in inflated_res.items():
            # print('{} ---> {}'.format(k, v))
            # indicate match found
            if len(k) > 1:
                if k[:2] == ('ClaimInvestigationAddRs', 'MatchDetails'):
                    break
        else:
            print('no match')
            case_of_no_match = True

        # if TRUE then it is multi; otherwise single or no MatchDetails
        # TODO: to detect no Match case, loop through all keys
        # and do key_01[:2] == ('ClaimInvestigationAddRs', 'MatchDetails')
        if ('ClaimInvestigationAddRs', 'MatchDetails') in inflated_res:
            print('multiple matches')
            iso_results.extend(digest_multi_matches(inflated_res))
        elif not case_of_no_match:
            print('single match')
            iso_results.append(digest_single_match(inflated_res))

    return iso_results

def digest_single_match(iso):
    row = {}
    
    discover = iso.get
    row['Response_Id'] = discover(
        ('ClaimInvestigationAddRs',
         'RqUID'))

    row['ISO_Response_Date'] = discover(
        ('ClaimInvestigationAddRs',
         'TransactionResponseDt'))
    row['MLX_Policy_Number'] = discover(
        ('ClaimInvestigationAddRs',
         'Policy',
         'PolicyNumber'))

    row['Match_Insurer_Policy_Number'] = discover(
        ('ClaimInvestigationAddRs',
         'MatchDetails',
         'Policy',
         'PolicyNumber'))

    row['Match_Insurer_Effective_Date'] = discover(
        ('ClaimInvestigationAddRs',
         'MatchDetails',
         'Policy',
         'ContractTerm',
         'EffectiveDt'))

    row['Match_Insurer_Term_Date'] = discover(
        ('ClaimInvestigationAddRs',
         'MatchDetails',
         'Policy',
         'ContractTerm',
         'ExpirationDt'))

    if ('ClaimInvestigationAddRs',
         'MatchDetails',
         'Policy',
         'LOBCd') in iso:
        row['Match_Insurer_LOB'] = discover(
            ('ClaimInvestigationAddRs',
             'MatchDetails',
             'Policy',
             'LOBCd'))    
    else:
        row['Match_Insurer_LOB'] = discover(
            ('ClaimInvestigationAddRs',
             'MatchDetails',
             'Policy',
             'LOBCd',
             '#text'))

    row['Match_Insurer_Name'] = discover(
        ('ClaimInvestigationAddRs',
         'MatchDetails',
         'Policy',
         'MiscParty',
         'GeneralPartyInfo',
         'NameInfo',
         'CommlName',
         'CommercialName'))

    row['Match_Insurer_Addr1'] = discover(
        ('ClaimInvestigationAddRs',
         'MatchDetails',
         'Policy',
         'MiscParty',
         'GeneralPartyInfo',
         'Addr',
         'Addr1'))

    row['Match_Insurer_Addr2'] = discover(
        ('ClaimInvestigationAddRs',
         'MatchDetails',
         'Policy',
         'MiscParty',
         'GeneralPartyInfo',
         'Addr',
         'Addr2'))

    row['Match_Insurer_City'] = discover(
        ('ClaimInvestigationAddRs',
         'MatchDetails',
         'Policy',
         'MiscParty',
         'GeneralPartyInfo',
         'Addr',
         'City'))

    row['Match_Insurer_State'] = discover(
        ('ClaimInvestigationAddRs',
         'MatchDetails',
         'Policy',
         'MiscParty',
         'GeneralPartyInfo',
         'Addr',
         'StateProvCd'))

    row['Match_Insurer_Zip'] = discover(
        ('ClaimInvestigationAddRs',
         'MatchDetails',
         'Policy',
         'MiscParty',
         'GeneralPartyInfo',
         'Addr',
         'PostalCode'))

    row['Match_Insurer_Phone'] = discover(
        ('ClaimInvestigationAddRs',
         'MatchDetails',
         'Policy',
         'MiscParty',
         'GeneralPartyInfo',
         'Communications',
         'PhoneInfo',
         'PhoneNumber'))

    row['Match_Insurer_Role_Code'] = discover(
        ('ClaimInvestigationAddRs',
         'MatchDetails',
         'Policy',
         'MiscParty',
         'MiscPartyInfo',
         'MiscPartyRoleCd'))

    row['ISO_Agency_Id'] = discover(
        ('ClaimInvestigationAddRs',
         'MatchDetails',
         'ClaimsOccurrence',
         'ItemIdInfo',
         'AgencyId'))
    
    row['ISO_Insured_Id'] = discover(
        ('ClaimInvestigationAddRs',
         'MatchDetails',
         'ClaimsOccurrence',
         'ItemIdInfo',
         'InsurerId'))

    row['Loss_Date'] = discover(
        ('ClaimInvestigationAddRs',
         'MatchDetails',
         'ClaimsOccurrence',
         'LossDt'))

    row['Loss_Time'] = discover(
        ('ClaimInvestigationAddRs',
         'MatchDetails',
         'ClaimsOccurrence',
         'LossTime'))

    row['Loss_Description'] = discover(
        ('ClaimInvestigationAddRs',
         'MatchDetails',
         'ClaimsOccurrence',
         'IncidentDesc'))

    row['Loss_Address_1'] = discover(
        ('ClaimInvestigationAddRs',
         'MatchDetails',
         'ClaimsOccurrence',
         'Addr',
         'Addr1'))

    row['Loss_City'] = discover(
        ('ClaimInvestigationAddRs',
         'MatchDetails',
         'ClaimsOccurrence',
         'Addr',
         'City'))

    row['Loss_State'] = discover(
        ('ClaimInvestigationAddRs',
         'MatchDetails',
         'ClaimsOccurrence',
         'Addr',
         'StateProvCd'))

    claimsParty = discover(
        ('ClaimInvestigationAddRs',
         'MatchDetails',
         'ClaimsParty'))
    if claimsParty:    # maybe one or many
        if not isinstance(claimsParty, list):
            claimsParty = list(claimsParty)

        row_claimsParty = digest_claimsParty(claimsParty)
        row.update(row_claimsParty)

    adjusterParty = discover(
        ('ClaimInvestigationAddRs',
         'MatchDetails',
         'AdjusterParty'))
    # TODO: need to rework this later
    if adjusterParty:    # maybe zero or many
        print(adjusterParty)
        if not isinstance(adjusterParty, list):
            adjusterParty = list(adjusterParty)

        row_adjusterParty = digest_adjusterPartys(adjusterParty)
        row.update(row_adjusterParty)
    else:    # TODO: revisit: in case there is no adjusterParty
        adjusterParty = flush(iso)
        for k, v in adjusterParty.items():
            print('{} ---> {}'.format(k, v))

        row_adjusterParty = digest_adjusterParty(adjusterParty, prefix=('ClaimInvestigationAddRs', 'MatchDetails'))            
        row.update(row_adjusterParty)


    return scrub_data_value(row)

def digest_claimsParty(claimsParty):
    row = {}
    for index, claimsParty in enumerate(claimsParty):
        claimsParty = flush(claimsParty)
        #for k, v in claimsParty.items():
        #    print('{} ---> {}'.format(k, v))
        row['Claims_Party_{}_Last_Name'.format(index+1)] = (
            claimsParty.get(
                ('GeneralPartyInfo',
                 'NameInfo',
                 'PersonName',
                 'Surname')))

        row['Claims_Party_{}_First_Name'.format(index+1)] = (
            claimsParty.get(
                ('GeneralPartyInfo',
                 'NameInfo',
                 'PersonName',
                 'GivenName')))

        row['Claims_Party_{}_Commercial_Name'.format(index+1)] = (
            claimsParty.get(
                ('GeneralPartyInfo',
                 'NameInfo',
                 'CommlName',
                 'CommercialName')))

        row['Claims_Party_{}_Id_Type'.format(index+1)] = (
            claimsParty.get(
                ('GeneralPartyInfo',
                 'TaxIdentity',
                 'TaxIdTypeCd')))

        row['Claims_Party_{}_Id_number'.format(index+1)] = (
            claimsParty.get(
                ('GeneralPartyInfo',
                 'TaxIdentity',
                 'TaxId')))

        row['Claims_Party_{}_Id_State'.format(index+1)] = (
            claimsParty.get(
                ('GeneralPartyInfo',
                 'TaxIdentity',
                 'StateProvCd')))

        row['Claims_Party_{}_Gender'.format(index+1)] = (
            claimsParty.get(
                ('GeneralPartyInfo',
                 'PersonInfo',
                 'GenderCd')))            

        row['Claims_Party_{}_Birth_Date'.format(index+1)] = (
            claimsParty.get(
                ('GeneralPartyInfo',
                 'PersonInfo',
                 'BirthDt')))

        # TODO: revisit this with Matt
        row['Claims_Party_{}_Injury_Info_1'.format(index+1)] = (
            claimsParty.get(
                ('GeneralPartyInfo',
                 'ClaimsInjuredInfo',
                 'ClaimsInjury',
                 'InjuryNatureDesc')))

        # TODO: revisit this with Matt
        row['Claims_Party_{}_Injury_Info_2'.format(index+1)] = (
            claimsParty.get(
                ('GeneralPartyInfo',
                 'ClaimsInjuredInfo',
                 'ClaimsInjury',
                 'InjuryNatureDesc')))

        row['Claims_Party_{}_Address_1'.format(index+1)] = (
            claimsParty.get(
                ('GeneralPartyInfo',
                 'Addr',
                 'Addr1')))

        row['Claims_Party_{}_City'.format(index+1)] = (
            claimsParty.get(
                ('GeneralPartyInfo',
                 'Addr',
                 'City')))

        row['Claims_Party_{}_State'.format(index+1)] = (
            claimsParty.get(
                ('GeneralPartyInfo',
                 'Addr',
                 'StateProvCd')))            
     
        row['Claims_Party_{}_Zip'.format(index+1)] = (
            claimsParty.get(
                ('GeneralPartyInfo',
                 'Addr',
                 'PostalCode')))

        row['Claims_Party_{}_Comm_1_type'.format(index+1)] = (
            claimsParty.get(
                ('GeneralPartyInfo',
                 'Communications',
                 'PhoneInfo',
                 'PhoneTypeCd')))

        row['Claims_Party_{}_Comm_1_use'.format(index+1)] = (
            claimsParty.get(
                ('GeneralPartyInfo',
                 'Communications',
                 'PhoneInfo',
                 'CommunicationUseCd')))             

        row['Claims_Party_{}_Comm_1_number'.format(index+1)] = (
            claimsParty.get(
                ('GeneralPartyInfo',
                 'Communications',
                 'PhoneInfo',
                 'PhoneNumber')))

        # maybe unicode or dict 
        claimsPartyRoleCd = (
            claimsParty.get(
                ('ClaimsPartyInfo',
                 'ClaimsPartyRoleCd')))
        if not claimsPartyRoleCd:
            claimsPartyRoleCd = (
                claimsParty.get(
                    ('ClaimsPartyInfo',
                     'ClaimsPartyRoleCd',   
                     '#text')))
        row['Claims_Party_{}_Role_Code'.format(index+1)] = (
            claimsPartyRoleCd)

    return row

def digest_adjusterPartys(adjusterPartys):
    row = {}
    # print(adjusterParty_list)
    for index, adjusterParty in enumerate(adjusterPartys):
        adjusterParty = flush(adjusterParty)
        # for k, v in adjusterParty.items():
        #     print('{} ---> {}'.format(k, v))
        row['Adjuster_Party_{}_Commercial_Name'.format(index+1)] = (
            adjusterParty.get(
                ('GeneralPartyInfo',
                 'NameInfo',
                 'CommlName',
                 'CommercialName')))
        
        row['Adjuster_Party_{}_Last_Name'.format(index+1)] = (
            adjusterParty.get(
                ('GeneralPartyInfo',
                 'NameInfo',
                 'PersonName',
                 'Surname')))

        row['Adjuster_Party_{}_First_Name'.format(index+1)] = (
            adjusterParty.get(
                ('GeneralPartyInfo',
                 'NameInfo',
                 'PersonName',
                 'GivenName')))

        row['Adjuster_Party_{}_Comm_1_type'.format(index+1)] = (
            adjusterParty.get(
                ('GeneralPartyInfo',
                 'Communications',
                 'PhoneInfo',
                 'PhoneTypeCd')))

        row['Adjuster_Party_{}_Comm_1_use'.format(index+1)] = (
            adjusterParty.get(
                ('GeneralPartyInfo',
                 'Communications',
                 'PhoneInfo',
                 'CommunicationUseCd')))

        row['Adjuster_Party_{}_Comm_1_number'.format(index+1)] = (
            adjusterParty.get(
                ('GeneralPartyInfo',
                 'Communications',
                 'PhoneInfo',
                 'PhoneNumber')))
              
    return row

def digest_adjusterParty(adjusterParty, prefix=None):
    row = {}
    index = 0
    # pref = prefix if prefix else ()
    # test_key = (pref + ('AdjusterParty',
    #          'GeneralPartyInfo',
    #          'NameInfo',
    #          'CommlName',
    #          'CommercialName'),)
    # print('...{}...'.format(test_key))
    # print(adjusterParty.get(test_key))
    # for k, v in adjusterParty.items():
    #    print('{} ---> {}'.format(k, v))
    if prefix:
        row['Adjuster_Party_{}_Commercial_Name'.format(index+1)] = (
            adjusterParty.get((pref +
                ('AdjusterParty',
                 'GeneralPartyInfo',
                 'NameInfo',
                 'CommlName',
                 'CommercialName'),)))
        
        row['Adjuster_Party_{}_Last_Name'.format(index+1)] = (
            adjusterParty.get((pref +
                ('AdjusterParty',
                 'GeneralPartyInfo',
                 'NameInfo',
                 'PersonName',
                 'Surname'),)))

        row['Adjuster_Party_{}_First_Name'.format(index+1)] = (
            adjusterParty.get((pref +
                ('AdjusterParty',
                 'GeneralPartyInfo',
                 'NameInfo',
                 'PersonName',
                 'GivenName'),)))

        row['Adjuster_Party_{}_Comm_1_type'.format(index+1)] = (
            adjusterParty.get((pref +
                ('AdjusterParty',
                 'GeneralPartyInfo',
                 'Communications',
                 'PhoneInfo',
                 'PhoneTypeCd'),)))

        row['Adjuster_Party_{}_Comm_1_use'.format(index+1)] = (
            adjusterParty.get((pref +
                ('AdjusterParty',
                 'GeneralPartyInfo',
                 'Communications',
                 'PhoneInfo',
                 'CommunicationUseCd'),)))

        row['Adjuster_Party_{}_Comm_1_number'.format(index+1)] = (
            adjusterParty.get((pref +
                ('AdjusterParty',
                 'GeneralPartyInfo',
                 'Communications',
                 'PhoneInfo',
                 'PhoneNumber'),)))
    else:
        row['Adjuster_Party_{}_Commercial_Name'.format(index+1)] = (
            adjusterParty.get(
                ('GeneralPartyInfo',
                 'NameInfo',
                 'CommlName',
                 'CommercialName')))
        
        row['Adjuster_Party_{}_Last_Name'.format(index+1)] = (
            adjusterParty.get(
                ('GeneralPartyInfo',
                 'NameInfo',
                 'PersonName',
                 'Surname')))

        row['Adjuster_Party_{}_First_Name'.format(index+1)] = (
            adjusterParty.get(
                ('GeneralPartyInfo',
                 'NameInfo',
                 'PersonName',
                 'GivenName')))

        row['Adjuster_Party_{}_Comm_1_type'.format(index+1)] = (
            adjusterParty.get(
                ('GeneralPartyInfo',
                 'Communications',
                 'PhoneInfo',
                 'PhoneTypeCd')))

        row['Adjuster_Party_{}_Comm_1_use'.format(index+1)] = (
            adjusterParty.get(
                ('GeneralPartyInfo',
                 'Communications',
                 'PhoneInfo',
                 'CommunicationUseCd')))

        row['Adjuster_Party_{}_Comm_1_number'.format(index+1)] = (
            adjusterParty.get(
                ('GeneralPartyInfo',
                 'Communications',
                 'PhoneInfo',
                 'PhoneNumber')))            
              
    return row        

def digest_mm_adjusterParty(adjusterParty):
    nameInfos = adjusterParty.get(
        ('AdjusterParty',
        'GeneralPartyInfo',
        'NameInfo'))

    row = {}
    index = 0
    # TODO: 'NameInfo' can be multiple
    if isinstance(nameInfos, list):
        # TODO: check basics
        nameInfo_1 = flush(nameInfos[0])
        row['Adjuster_Party_{}_Commercial_Name'.format(index+1)] = (
            nameInfo_1.get(
                ('CommlName',
                 'CommercialName')))
        if len(nameInfos) >= 2:
            nameInfo_2 = flush(nameInfos[1])
            row['Adjuster_Party_{}_Last_Name'.format(index+1)] = (
                nameInfo_2.get(
                    ('PersonName',
                     'Surname')))

            row['Adjuster_Party_{}_First_Name'.format(index+1)] = (
                nameInfo_2.get(
                    ('PersonName',
                     'GivenName')))
    else:
        row['Adjuster_Party_{}_Commercial_Name'.format(index+1)] = (
            adjusterParty.get(
                ('AdjusterParty',
                 'GeneralPartyInfo',
                 'NameInfo',
                 'CommlName',
                 'CommercialName')))
        
        row['Adjuster_Party_{}_Last_Name'.format(index+1)] = (
            adjusterParty.get(
                ('AdjusterParty',
                 'GeneralPartyInfo',
                 'NameInfo',
                 'PersonName',
                 'Surname')))

        row['Adjuster_Party_{}_First_Name'.format(index+1)] = (
            adjusterParty.get(
                ('AdjusterParty',
                 'GeneralPartyInfo',
                 'NameInfo',
                 'PersonName',
                 'GivenName')))        

    row['Adjuster_Party_{}_Comm_1_type'.format(index+1)] = (
        adjusterParty.get(
            ('AdjusterParty',
             'GeneralPartyInfo',
             'Communications',
             'PhoneInfo',
             'PhoneTypeCd')))

    row['Adjuster_Party_{}_Comm_1_use'.format(index+1)] = (
        adjusterParty.get(
            ('AdjusterParty',
             'GeneralPartyInfo',
             'Communications',
             'PhoneInfo',
             'CommunicationUseCd')))

    row['Adjuster_Party_{}_Comm_1_number'.format(index+1)] = (
        adjusterParty.get(
            ('AdjusterParty',
             'GeneralPartyInfo',
             'Communications',
             'PhoneInfo',
             'PhoneNumber')))            
              
    return row         


def digest_multi_matches(iso):
    result = []
    COMMON_Response_Id = iso.get(
        ('ClaimInvestigationAddRs',
         'RqUID'))
    COMMON_ISO_Response_Date = iso.get(
        ('ClaimInvestigationAddRs',
         'TransactionResponseDt'))
    COMMON_MLX_Policy_Number = iso.get(
        ('ClaimInvestigationAddRs',
         'Policy',
         'PolicyNumber'))

    match_details = iso.get(('ClaimInvestigationAddRs', 'MatchDetails'))
    print(len(match_details))
    for match_detail in match_details:
        md = flush(match_detail)
        discover = md.get
        # for k, v in md.items():
        #    print('{} ---> {}'.format(k, v))

        row = {}

        row['Response_Id'] = COMMON_Response_Id
        row['ISO_Response_Date'] = COMMON_ISO_Response_Date
        row['MLX_Policy_Number'] = COMMON_MLX_Policy_Number

        # packing away ...
        row['Match_Insurer_Policy_Number'] = discover(
        ('Policy',
         'PolicyNumber'))

        row['Match_Insurer_Effective_Date'] = discover(
            ('Policy',
             'ContractTerm',
             'EffectiveDt'))

        row['Match_Insurer_Term_Date'] = discover(
            ('Policy',
             'ContractTerm',
             'ExpirationDt'))

        if ('Policy', 'LOBCd') in md:
            row['Match_Insurer_LOB'] = discover(
                ('Policy',
                 'LOBCd'))    
        else:
            row['Match_Insurer_LOB'] = discover(
                ('Policy',
                 'LOBCd',
                 '#text'))

        row['Match_Insurer_Name'] = discover(
            ('Policy',
             'MiscParty',
             'GeneralPartyInfo',
             'NameInfo',
             'CommlName',
             'CommercialName'))

        row['Match_Insurer_Addr1'] = discover(
            ('Policy',
             'MiscParty',
             'GeneralPartyInfo',
             'Addr',
             'Addr1'))

        row['Match_Insurer_Addr2'] = discover(
            ('Policy',
             'MiscParty',
             'GeneralPartyInfo',
             'Addr',
             'Addr2'))

        row['Match_Insurer_City'] = discover(
            ('Policy',
             'MiscParty',
             'GeneralPartyInfo',
             'Addr',
             'City'))

        row['Match_Insurer_State'] = discover(
            ('Policy',
             'MiscParty',
             'GeneralPartyInfo',
             'Addr',
             'StateProvCd'))

        row['Match_Insurer_Zip'] = discover(
            ('Policy',
             'MiscParty',
             'GeneralPartyInfo',
             'Addr',
             'PostalCode'))

        row['Match_Insurer_Phone'] = discover(
            ('Policy',
             'MiscParty',
             'GeneralPartyInfo',
             'Communications',
             'PhoneInfo',
             'PhoneNumber'))

        row['Match_Insurer_Role_Code'] = discover(
            ('Policy',
             'MiscParty',
             'MiscPartyInfo',
             'MiscPartyRoleCd'))

        row['ISO_Agency_Id'] = discover(
            ('ClaimsOccurrence',
             'ItemIdInfo',
             'AgencyId'))

        row['ISO_Insured_Id'] = discover(
            ('ClaimsOccurrence',
             'ItemIdInfo',
             'InsurerId'))

        row['Loss_Date'] = discover(
            ('ClaimsOccurrence',
             'LossDt'))

        row['Loss_Time'] = discover(
            ('ClaimsOccurrence',
             'LossTime'))

        row['Loss_Description'] = discover(
            ('ClaimsOccurrence',
             'IncidentDesc'))

        row['Loss_Address_1'] = discover(
            ('ClaimsOccurrence',
             'Addr',
             'Addr1'))

        row['Loss_City'] = discover(
            ('ClaimsOccurrence',
             'Addr',
             'City'))

        row['Loss_State'] = discover(
            ('ClaimsOccurrence',
             'Addr',
             'StateProvCd'))

        claimsParty = discover(('ClaimsParty',))
        if claimsParty:
            if not isinstance(claimsParty, list):
                claimsParty = list(claimsParty)

            row_claimsParty = digest_claimsParty(claimsParty)
            row.update(row_claimsParty)


        # AdjusterParty is one for the most part
        # TODO: also handle multiple AdjusterPartys
        adjusterParty = discover(('AdjusterParty',))
        if adjusterParty:
            if not isinstance(adjusterParty, list):
                adjusterParty = list(adjusterParty)

            row_adjusterParty = digest_adjusterPartys(adjusterParty)
            row.update(row_adjusterParty)
        else:
            row_adjusterParty = digest_mm_adjusterParty(md)
            row.update(row_adjusterParty)

        result.append(scrub_data_value(row))
    return result


if __name__ == '__main__':
    INPUT_DIR = 'C://Users//yann.yu//Documents//tips//how2medlytix//ISO_project//test_run_06_29_2017//input//'
    OUTPUT_DIR = 'C://Users//yann.yu//Documents//tips//how2medlytix//ISO_project//test_run_06_29_2017//output//'
    if os.path.isdir(INPUT_DIR) and os.path.isdir(OUTPUT_DIR):
        for filename in glob.glob(os.path.join(INPUT_DIR, '*.xml')):
            # do your stuff
            print(filename)
            resp_file = filename 
            # resp_file = 'Multiple_Matches.xml'
            # resp_file = 'Matt_WC_response.xml'
            # resp_file = 'Matt_WC_response_test.xml'
            my_resp_file = os.path.basename(resp_file)
            variation = my_resp_file[:-4]
            output_file = 'iso_MLX_test_{}.txt'.format(variation)
            if os.path.isfile(resp_file):
                iso_results = digest_iso_resp(resp_file)
                write(os.path.join(OUTPUT_DIR, output_file), iso_results)
            else:
                raise OSError(2, 'No such file or directory', resp_file)
    else:
        raise OSError(2, 'No such file or directory', '{} or {}'.format(INPUT_DIR, OUTPUT_DIR))