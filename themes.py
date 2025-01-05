from PIL import Image, ImageDraw, ImageFont
import random

rainbow_theme = {
    'theme_id':'rainbow',
    'img_path':'assets/backgrounds/rainbow_bg.png',
    'presenting_font_color':(255,255,255),
    'title_font_color':(255,255,255),
    'music_festival_font_color':(255,255,255),
    'day_color_bg':(0,0,0),
    'day_font_color':(255,255,255),
    'lineup_font_color':(255,255,255),
    'title_font_size':60,
    'lineup_font':'assets/fonts/PirataOne-Regular.ttf',
    'title_font':'assets/fonts/PirataOne-Regular.ttf',
    'subtitle_font':'assets/fonts/Quicksand-VariableFont_wght.ttf',
    'headliner1_font_size':55,
    'headliner2_font_size':45,
    'headliner3_font_size':35,
    'headliner4_font_size':30}

forest_theme = {
    'theme_id':'forest',
    'img_path':'assets/backgrounds/forest_bg.png',
    'presenting_font_color':(0,0,0),
    'title_font_color':(0,0,0),
    'music_festival_font_color':(0,0,0),
    'day_color_bg':(0, 0, 128),
    'day_font_color':(255,255,255),
    'lineup_font_color':(0,0,0),
    'title_font_size':48,
    'lineup_font':'assets/fonts/RubikBubbles-Regular.ttf',
    'title_font':'assets/fonts/RubikBubbles-Regular.ttf',
    'subtitle_font':'assets/fonts/LifeSavers-Regular.ttf',
    'headliner1_font_size':45,
    'headliner2_font_size':35,
    'headliner3_font_size':25,
    'headliner4_font_size':20}

trippy_theme = {
    'theme_id':'trippy',
    'img_path':'assets/backgrounds/trippy_bg.png',
    'presenting_font_color':(0,61,49),
    'title_font_color':(0,61,49),
    'music_festival_font_color':(0,61,49),
    'day_color_bg':(0,61,49),
    'day_font_color':(255,255,255),
    'lineup_font_color':(0,61,49),
    'title_font_size':48,
    'lineup_font':'assets/fonts/Kalnia-VariableFont_wdth,wght.ttf',
    'title_font':'assets/fonts/Kalnia-VariableFont_wdth,wght.ttf',
    'subtitle_font':'assets/fonts/Oswald-VariableFont_wght.ttf',
    'headliner1_font_size':38,
    'headliner2_font_size':28,
    'headliner3_font_size':18,
    'headliner4_font_size':13}

sunset_theme = {
    'theme_id':'sunset',
    'img_path':'assets/backgrounds/sunset_bg.png',
    'presenting_font_color':(0,0,0),
    'title_font_color':(250,141,36),
    'music_festival_font_color':(0,0,0),
    'day_color_bg':(250,141,36),
    'day_font_color':(255,255,255),
    'lineup_font_color':(0,0,0),
    'title_font_size':48,
    'lineup_font':'assets/fonts/TitanOne-Regular.ttf',
    'title_font':'assets/fonts/TitanOne-Regular.ttf',
    'subtitle_font':'assets/fonts/Oswald-VariableFont_wght.ttf',
    'headliner1_font_size':45,
    'headliner2_font_size':35,
    'headliner3_font_size':25,
    'headliner4_font_size':20}

pastel_theme = {
    'theme_id':'pastel',
    'img_path':'assets/backgrounds/pastel_bg.png',
    'presenting_font_color':(0,61,49),
    'title_font_color':(0,61,49),
    'music_festival_font_color':(0,61,49),
    'day_color_bg':(0,61,49),
    'day_font_color':(255,255,255),
    'lineup_font_color':(0,61,49),
    'title_font_size':48,
    'lineup_font':'assets/fonts/ChelseaMarket-Regular.ttf',
    'title_font':'assets/fonts/ChelseaMarket-Regular.ttf',
    'subtitle_font':'assets/fonts/Oswald-VariableFont_wght.ttf',
    'headliner1_font_size':45,
    'headliner2_font_size':35,
    'headliner3_font_size':25,
    'headliner4_font_size':20,
}

checker_theme = {
    'theme_id':'checker',
    'img_path':'assets/backgrounds/checker_bg.png', # change
    'presenting_font_color':(0,61,49), # keep
    'title_font_color':(0,61,49), # keep
    'music_festival_font_color':(0,61,49),
    'day_color_bg':(255, 189, 89),
    'day_font_color':(255,255,255),
    'lineup_font_color':(0,61,49),
    'title_font_size':52,
    'lineup_font':'assets/fonts/Barriecito-Regular.ttf',
    'title_font':'assets/fonts/Barriecito-Regular.ttf',
    'subtitle_font':'assets/fonts/Oswald-VariableFont_wght.ttf',
    'headliner1_font_size':45,
    'headliner2_font_size':35,
    'headliner3_font_size':25,
    'headliner4_font_size':20,
}

galaxy_theme = {
    'theme_id':'galaxy',
    'img_path':'assets/backgrounds/galaxy_bg.png', 
    'presenting_font_color':(255,255,255), 
    'title_font_color':(255,255,255),
    'music_festival_font_color':(255,255,255),
    'day_color_bg':(255, 189, 89, 0),
    'day_font_color':(255,255,255),
    'lineup_font_color':(255,255,255),
    'title_font_size':52,
    'lineup_font':'assets/fonts/ReggaeOne-Regular.ttf',
    'title_font':'assets/fonts/TenorSans-Regular.ttf',
    'subtitle_font':'assets/fonts/TenorSans-Regular.ttf',
    'headliner1_font_size':45,
    'headliner2_font_size':35,
    'headliner3_font_size':25,
    'headliner4_font_size':20,
}

def get_text_length(coords,text,font):
    img = Image.open('assets/backgrounds/rainbow_bg.png')
    draw = ImageDraw.Draw(img)
    rect = draw.textbbox(coords, text, font=font)
    len = rect[2]-rect[0]
    return(len)

def get_font_size(coords,text,theme_font,font_size,theme_id):
    # Create the font
    font = ImageFont.truetype(theme_font, size=font_size)
    # initialize new font size
    new_font_size = font_size
    # calculate length
    length = get_text_length(coords,text,font)
    # check if length is longer than width
    if length > 590:
        # store length
        new_length = length
        while new_length > 590:
            # make font size smaller
            new_font_size = new_font_size - 2
            # create new smaller font
            new_font = ImageFont.truetype(theme_font, size=new_font_size)
            # recheck length
            new_length = get_text_length(coords,text,new_font)
        # return amount that needs to be sutracted from font
        return(new_font_size)
    else:
        # return original font size
        return(font_size)
            
def get_font(font_path,text,font_size,theme_id):
    coords=(0,0)
    # get font
    result = ImageFont.truetype(font_path, size=get_font_size(coords,text,font_path,font_size,theme_id))
    # check if variation needs to be changed
    if theme_id == 'trippy':
        result.set_variation_by_name('Bold') 
    return(result)

def create_poster(theme_dict,theme_id,artist_names,festival_name,username,n_clicks,session_id):
    #define height, width
    width, height = 600,800
    #load in image and create drawing
    img = Image.open(theme_dict['img_path'])
    draw = ImageDraw.Draw(img)

    #Presenting text
    presenting_font = ImageFont.truetype(theme_dict['subtitle_font'], size=20)
    draw.text((width/2, 70), 'PRESENTING', font=presenting_font, anchor="mt",fill=theme_dict['presenting_font_color'])

    #Festival name
    title_font = ImageFont.truetype(theme_dict['title_font'],size=theme_dict['title_font_size'])
    if theme_id == 'trippy':
        title_font.set_variation_by_name('Bold')
    draw.text((width/2, 105), festival_name, font=get_font(theme_dict['title_font'],festival_name,theme_dict['title_font_size'],theme_id), anchor="mt",fill=theme_dict['title_font_color'])

    #Music Festival Text
    music_festival_font = ImageFont.truetype(theme_dict['subtitle_font'], size=30)
    draw.text((width/2, 180), 'MUSIC FESTIVAL', font=music_festival_font, anchor="mt",fill=theme_dict['music_festival_font_color'])

    #Draw rectangles
    draw.rectangle([(225, 260), (375, 295)],fill=theme_dict['day_color_bg'],outline=theme_dict['day_color_bg'])

    draw.rectangle([(225, 510), (375, 545)],fill=theme_dict['day_color_bg'],outline=theme_dict['day_color_bg'])

    #Saturday Text
    day_font = ImageFont.truetype(theme_dict['subtitle_font'], size=20)
    draw.text((width/2, 270), 'SATURDAY', font=day_font, anchor="mt",fill=theme_dict['day_font_color'])
    
    #Sunday Text
    draw.text((width/2, 520), 'SUNDAY', font=day_font, anchor="mt",fill=theme_dict['day_font_color'])
    
    #add top headliners
    draw.text((width/2, 320), artist_names[0], font=get_font(theme_dict['lineup_font'],artist_names[0],theme_dict['headliner1_font_size'],theme_id), anchor="mt",fill=theme_dict['lineup_font_color'])
    draw.text((width/2, 570), artist_names[1], font=get_font(theme_dict['lineup_font'],artist_names[1],theme_dict['headliner1_font_size'],theme_id), anchor="mt",fill=theme_dict['lineup_font_color'])

    #add 2nd headliners
    second_headline1 = str(artist_names[2])+str('   ')+str(artist_names[3])
    second_headline2 = str(artist_names[4])+str('   ')+str(artist_names[5])
    draw.text((width/2, 370), second_headline1, font=get_font(theme_dict['lineup_font'],second_headline1,theme_dict['headliner2_font_size'],theme_id), anchor="mt",fill=theme_dict['lineup_font_color'])
    draw.text((width/2, 620), second_headline2, font=get_font(theme_dict['lineup_font'],second_headline2,theme_dict['headliner2_font_size'],theme_id), anchor="mt",fill=theme_dict['lineup_font_color'])

    #add 3rd headliners
    third_headline1 = str(artist_names[6])+str('   ')+str(artist_names[7])+str('   ')+str(artist_names[8])
    third_headline2 = str(artist_names[9])+str('   ')+str(artist_names[10])+str('   ')+str(artist_names[11])
    draw.text((width/2, 410),third_headline1,font=get_font(theme_dict['lineup_font'],third_headline1,theme_dict['headliner3_font_size'],theme_id),anchor="mt",fill=theme_dict['lineup_font_color'])
    draw.text((width/2, 660),third_headline2,font=get_font(theme_dict['lineup_font'],third_headline2,theme_dict['headliner3_font_size'],theme_id),anchor="mt",fill=theme_dict['lineup_font_color'])

    #add 4th headliners
    fourth_headline1 = str(artist_names[12])+str('   ')+str(artist_names[13])+str('   ')+str(artist_names[14])+str('   ')+str(artist_names[15])
    fourth_headline2 = str(artist_names[16])+str('   ')+str(artist_names[17])+str('   ')+str(artist_names[18])+str('   ')+str(artist_names[19])
    draw.text((width/2, 440),fourth_headline1,font=get_font(theme_dict['lineup_font'],fourth_headline1,theme_dict['headliner4_font_size'],theme_id),anchor="mt",fill=theme_dict['lineup_font_color'])
    draw.text((width/2, 690),fourth_headline2,font=get_font(theme_dict['lineup_font'],fourth_headline2,theme_dict['headliner4_font_size'],theme_id),anchor="mt",fill=theme_dict['lineup_font_color'])

    img_name = 'assets/poster_'+str(username)+'_'+session_id+'_'+str(n_clicks)+'.png'
    img.save(img_name)