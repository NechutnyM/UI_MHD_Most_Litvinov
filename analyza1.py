import arcpy
import os
import statistics

import arcpy, os, statistics
from PIL import Image
tato_slozka = os.path.dirname(os.path.realpath(__file__))
arcpy.env.overwriteOutput = 1
arcpy.env.qualifiedFieldNames = 0

def filtrace_bodu_cas(body_shp, start, konec, dny, vystup):
    arcpy.MakeFeatureLayer_management(body_shp, "fl_body")
    arcpy.CopyFeatures_management("fl_body", "fl_body_dny")
    arcpy.DeleteFeatures_management("fl_body_dny")
    sql_podminka = f"EXTRACT(HOUR FROM TIME_DATE) >= {start} AND EXTRACT(HOUR FROM TIME_DATE) < {konec}"
    arcpy.SelectLayerByAttribute_management("fl_body", "NEW_SELECTION", sql_podminka)
    with arcpy.da.InsertCursor("fl_body_dny", "*") as insert_cursor:
        with arcpy.da.SearchCursor("fl_body", "*") as search_cursor:
            for row in search_cursor:
                datum = row[12]
                vse = row
                if datum.weekday() in dny:
                    insert_cursor.insertRow(vse)
    arcpy.CopyFeatures_management("fl_body_dny", vystup)
    return(vystup)

def filtrace_linky(vstup, zpr_linka, vystup):
    arcpy.MakeFeatureLayer_management(vstup, "fl_body")
    # definování výběrové podmínky
    query_expression = f"CISLO_LINKY = {zpr_linka}"
    arcpy.SelectLayerByAttribute_management("fl_body", "NEW_SELECTION", query_expression)
    arcpy.CopyFeatures_management("fl_body", vystup)
    return(vystup)


def spust_analyzu(gdb_path, output_folder, linka, dny, start, konec, delka_useku):
    import arcpy, os, statistics
    from PIL import Image
    tato_slozka = os.path.dirname(os.path.realpath(__file__))
    arcpy.env.workspace = rf"{tato_slozka}\MhdMost"
    arcpy.env.overwriteOutput = 1
    arcpy.env.qualifiedFieldNames = 0
    project_path = os.path.join(tato_slozka, 'project_aprx_mapy', 'project_most.aprx')
    uloziste_vrstev_slozka = os.path.join(tato_slozka, 'vzory_lyrx')
    vysledky_slozka = output_folder
    xid = 0
    
    vstup = rf'{gdb_path}\zpolohy_zkontrolovano'
    body_vybrana_linka = filtrace_linky(vstup, linka, rf'MhdMost\body_vybrana_linka')
    fc_body = filtrace_bodu_cas(body_vybrana_linka, start, konec, dny, rf"MhdMost\fc_body")


    #Výběr konkrétní linky a uložení její trasy do vybrana_linka.shp
    #_________________________________________________________________

    linky_cele = rf'{gdb_path}\linky_cele'
    feature_layer = "selected_features"
    arcpy.MakeFeatureLayer_management(linky_cele, feature_layer)

    query_expression = f"LINKA = {linka}"

    # definování výběrové podmínky
    arcpy.SelectLayerByAttribute_management(feature_layer, "NEW_SELECTION", query_expression)

    output_vyb_linka = 'vybrana_linka.shp'

    # nakopírování výběru do výsledného shapefilu
    arcpy.CopyFeatures_management(feature_layer, output_vyb_linka)
    arcpy.Delete_management(feature_layer)
    arcpy.management.Project(output_vyb_linka, 'vybrana_linka_proj.shp', 3857) #vytvoření stejné vrstvy v jiném zobrazení, aby bylo možné využít extent vrstvy pro zoomování finální mapy, ktreá je v souř. systému 3857 z důvodu podkladové mapy


    #Rozsekání dané linky po delka_useku metrech
    #_________________________________________________________________


    arcpy.MakeFeatureLayer_management("vybrana_linka.shp", 'input_layer')

    spatial_reference = arcpy.Describe("vybrana_linka.shp").spatialReference

    # Create the output shapefile
    arcpy.CreateFeatureclass_management(
        arcpy.env.workspace,
        "rozsekana_linka.shp",
        'POLYLINE',
        spatial_reference=spatial_reference
    )

    # vytvoření atributů - délka segmentu, průměrné zpoždění na daném segmentu - příprava k pozdějšímu naplnění daty, ID (z neznámého důvodu bez toho vhodně nefunguje následný spatial join)
    arcpy.AddField_management("rozsekana_linka.shp", 'Segm_Len', 'DOUBLE')
    arcpy.AddField_management(in_table = "rozsekana_linka.shp", field_name = 'Prum_Zpozd', field_type = 'DOUBLE', field_alias = "průměrné zpoždění v úseku")
    arcpy.AddField_management("rozsekana_linka.shp", 'ID_moje', 'INTEGER')


    with arcpy.da.InsertCursor("rozsekana_linka.shp", ['SHAPE@', 'Segm_Len', 'ID_moje']) as insert_cursor:
        with arcpy.da.SearchCursor('input_layer', ['SHAPE@', 'SHAPE@LENGTH']) as search_cursor:
            for row in search_cursor:
                original_line = row[0]
                line_length = row[1]

                # kolik segmentů bude třeba aby byly všechny (krom posledního) dlouhé delka_useku metrů?
                num_segments = int(line_length / delka_useku)

                # rozsekání linie na segmenty
                for i in range(num_segments):
                    xid +=1
                    start_distance = i * delka_useku
                    end_distance = (i + 1) * delka_useku if i < num_segments - 1 else line_length

                    segment = original_line.segmentAlongLine(start_distance, end_distance)
                    segment_length = segment.length

                    # Vložení do výstupu
                    insert_cursor.insertRow([segment, segment_length, xid])

    # vyčistění
    arcpy.Delete_management('input_layer')

    #Výběr zastávek
    #_________________________________________________________________
    zastavky_vyb = "selected_features"
    arcpy.MakeFeatureLayer_management(rf"{gdb_path}\zastavky_jednotne", zastavky_vyb)

    query_expression = f"LINKY LIKE '{linka},%' OR LINKY LIKE '%, {linka},%' OR LINKY LIKE '%, {linka}' OR LINKY LIKE '{linka}'"

    # definování výběrové podmínky
    arcpy.SelectLayerByAttribute_management(zastavky_vyb, "NEW_SELECTION", query_expression)

    output_vyb_zastavky = 'vybrane_zastavky.shp'

    # nakopírování výběru do výsledného shapefilu
    arcpy.CopyFeatures_management(zastavky_vyb, output_vyb_zastavky)
    arcpy.Delete_management(zastavky_vyb)

    #Práce s body
    #______________________
    cilove_stanice = set()
    with arcpy.da.SearchCursor(fc_body, ["CILOVA_Z_1"]) as cursor:
        for row in cursor:
            attribute_value = row[0]
            cilove_stanice.add(attribute_value)

    body = 'vybrane_body.shp'
    for cilova_stanice in cilove_stanice:
        query_expression = f"CISLO_LINK = {linka}"
        arcpy.SelectLayerByAttribute_management(fc_body, "NEW_SELECTION", query_expression)
        query_expression2 = f"CILOVA_Z_1 = '{cilova_stanice}'"
        arcpy.SelectLayerByAttribute_management(fc_body, "SUBSET_SELECTION", query_expression2)
        # nakopírování výběru do výsledného shapefilu
        arcpy.CopyFeatures_management(fc_body, body)

        #Přiřazení atributu o průměrném zpoždění jednotlivým segmentům linie
        #_________________________________________________________________

        linie = 'rozsekana_linka.shp'

        # Spatial join bodů a rozsekané linie
        arcpy.SpatialJoin_analysis(body, linie, 'body_linie_join.shp', "#", "#", "#", "CLOSEST")

        # body budu ukládat do slovníku na základě nejbližšího segmentu linie linky
        point_dict = {}

        with arcpy.da.SearchCursor('body_linie_join.shp', ['TARGET_FID', 'ID_moje', 'ZPOZDENI_M']) as sCur:
            for row in sCur:
                point_id = row[0]
                line_id = row[1]
                attribute_value = row[2]

                # Nový klíč dle segmentu, pokud zatím neexistuje
                if line_id not in point_dict:
                    point_dict[line_id] = []

                point_dict[line_id].append(attribute_value)

        # Průměry z hodnot zpoždění, které jsou uloženy jako list hodnot u každého segmentu (který - jehož id - je klíčem slovníku)
        with arcpy.da.UpdateCursor(linie, ['ID_moje', 'Prum_Zpozd']) as uCur:
            for row in uCur:
                line_id = row[0]

                if line_id in point_dict:
                    average_value = statistics.mean(point_dict[line_id])
                    row[1] = average_value
                    uCur.updateRow(row)

        #Tvorba a export mapy
        #_________________________________________________________________


        aprx = arcpy.mp.ArcGISProject(project_path)

        aprxMap = aprx.listMaps()[0]
        for vrstva in aprxMap.listLayers():
            aprxMap.removeLayer(vrstva)

        arcpy.MakeFeatureLayer_management('vybrana_linka_proj.shp', "proj_extent")
        arcpy.MakeFeatureLayer_management("rozsekana_linka.shp", f"průměrné zpoždění v úsecích trasy linky {linka} (sekundy)")
        arcpy.MakeFeatureLayer_management("vybrane_zastavky.shp", "zastávky")
        arcpy.SaveToLayerFile_management("proj_extent", fr'{uloziste_vrstev_slozka}\proj_extent_layer.lyrx', "ABSOLUTE")
        arcpy.SaveToLayerFile_management(f"průměrné zpoždění v úsecích trasy linky {linka} (sekundy)", fr'{uloziste_vrstev_slozka}\rozsekana_linka_layer.lyrx', "ABSOLUTE")
        arcpy.SaveToLayerFile_management("zastávky", fr'{uloziste_vrstev_slozka}\vybrane_zastavky_layer.lyrx', "ABSOLUTE")

        aprxMap.addBasemap("Light Gray Canvas")
        aprxMap.addDataFromPath(fr'{uloziste_vrstev_slozka}\proj_extent_layer.lyrx')
        aprxMap.addDataFromPath(fr'{uloziste_vrstev_slozka}\rozsekana_linka_layer.lyrx')
        aprxMap.addDataFromPath(fr'{uloziste_vrstev_slozka}\vybrane_zastavky_layer.lyrx')

        extent_layer = aprxMap.listLayers()[2]
        extent_layer_symbology = fr"{uloziste_vrstev_slozka}\extent_layer_vzor.lyrx"
        trasa_linky_layer = aprxMap.listLayers()[1]
        trasa_linky_symbology = fr"{uloziste_vrstev_slozka}\rozsekana_linka_vzor.lyrx"
        zastavky_layer = aprxMap.listLayers()[0]
        zastavky_symbology = fr"{uloziste_vrstev_slozka}\vybrane_zastavky_vzor.lyrx"
        aprxMap.spatialReference = arcpy.SpatialReference(3857)

        
        # nastavení přizoomování na zpracovanou linku
        aprxLayout = aprx.listLayouts()[1]
        nadpis = aprxLayout.listElements("TEXT_ELEMENT", "Text 1")[0]
        nadpis.text = f"na lince {linka} ve směru {cilova_stanice}"
        map_frame = aprxLayout.listElements('MAPFRAME_ELEMENT', "Map Frame")[0]
        map_frame.camera.setExtent(map_frame.getLayerExtent(extent_layer, False, True))
        scale_cur = map_frame.camera.scale
        scale_new = scale_cur * 1.1
        map_frame.camera.scale = scale_new

        extent_layer.visible = False #použito pouze pro nastavení extentu

        symbology = trasa_linky_layer.symbology
        if hasattr(symbology, 'classList'):
            for legend_class in symbology.classList:
                print(legend_class)

        #export do pdf
        aprxLayout.exportToPDF(fr"{vysledky_slozka}\layout_{linka}_usek_{delka_useku}_smer_{cilova_stanice}")
        print(f"proběhlo pro směr {cilova_stanice}")
        del aprx
        for vrstva in aprxMap.listLayers():
            aprxMap.removeLayer(vrstva)