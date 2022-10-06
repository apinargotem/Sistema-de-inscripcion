from requests import get, post



ENDPOINT= "/webservice/rest/server.php"

def rest_api_parameters(in_args,prefix='',out_dict=None):
    if out_dict==None:
        out_dict = {}
    if not type(in_args) in (list,dict):
        out_dict[prefix] = in_args
        return out_dict
    if prefix == '':
        prefix = prefix + '{0}'
    else:
        prefix = prefix + '[{0}]'
    if type(in_args)==list:
        for idx, item in enumerate(in_args):
            rest_api_parameters(item, prefix.format(idx), out_dict)
    elif type(in_args)==dict:
        for key, item in in_args.items():
            rest_api_parameters(item, prefix.format(key), out_dict)
    return out_dict

def call(fname, **kwargs):
    try:
        URL="http://localhost/moodle"
        KEY='7d74ab84998c2b1b4358eba0ccbb3e01'
        parameters = rest_api_parameters(kwargs)
        parameters.update({"wstoken": KEY, 'moodlewsrestformat': 'json', "wsfunction": fname})
        response = post(URL+ENDPOINT, parameters, verify=False)
        respuesta = response.json()
        response.close()
        return respuesta
    except Exception as ex:
        return[]
def BuscarCategorias(idnumber):
    return call('core_course_get_categories',criteria=[{'key':'idnumber','value':idnumber}],addsubcategories=0)


def BuscarCategoriasid(id):
    return call('core_course_get_categories',criteria=[{'key':'id','value':id}],addsubcategories=0)


def CrearCategorias(name,idnumber,description,parent=0):
    return call('core_course_create_categories', categories=[{'name': u'%s' % name, 'idnumber': idnumber, 'description': description, 'parent': parent}])

def BuscarCursos(vfield,vvalue):
    return call('core_course_get_courses_by_field',field=vfield,value=vvalue)


def CrearCursos(fullname,shortname,categoryid,idnumber,summary,startdate,enddate, numsections):
    maxbytes=20971520
    format='topics'
    showgrades=1
    newsitems=5

    showreports=1
    visible=1
    groupmode=0
    groupmodeforce=0

    return call('core_course_create_courses', courses=[{'fullname': u'%s' % fullname,
                                                        'shortname': shortname,
                                                        'categoryid': categoryid,
                                                        'idnumber': idnumber,
                                                        'summary': summary, 'format': format,
                                                        'showgrades': showgrades,
                                                        'newsitems': newsitems,
                                                        'startdate': startdate,
                                                        'enddate': enddate,
                                                        'numsections': numsections,
                                                        'maxbytes': maxbytes,
                                                        'showreports': showreports,
                                                        'visible': visible,
                                                        'groupmode': groupmode,
                                                        'groupmodeforce': groupmodeforce}])


def CrearCursosTarjeta( fullname, shortname, categoryid ,
                        idnumber, summary, startdate, enddate, numsections):
    """
    Estructura general

      //courses to create
    list of (
    object {
        fullname string   //full name
        shortname string   //course short name
        categoryid int   //category id
        idnumber string  Opcional //id number
        summary string  Opcional //summary
        summaryformat int  Valor por defecto para "1" //summary format (1 = HTML, 0 = MOODLE, 2 = PLAIN or 4 = MARKDOWN)
        startdate int  Opcional //timestamp when the course start
        enddate int  Opcional //timestamp when the course end
        numsections  Opcional //(deprecated, use courseformatoptions) number of weeks/topics
        hiddensections int  Opcional //(deprecated, use courseformatoptions) How the hidden sections in the course are displayed to students
        defaultgroupingid int  Valor por defecto para "0" //default grouping id
        enablecompletion int  Opcional //Enabled, control via completion and activity settings. Disabled,
                                                not shown in activity settings.
        completionnotify int  Opcional //1: yes 0: no
        lang string  Opcional //forced course language
        forcetheme string  Opcional //name of the force theme
        courseformatoptions  Opcional //additional options for particular course format
        list of (
            object {
            name string   //course format option name
            value string   //course format option value
            }
        )}
    )
    :param fullname:
    :param shortname:
    :param categoryid:
    :param idnumber:
    :param summary:
    :param startdate:
    :param enddate:
    :return:
    """
    # VARIABLES CON VALORES POR DEFECTO

    maxbytes = 10485760 # Valor por defecto para "0" //largest size of file that can be uploaded into the course
    format = 'remuiformat' # Valor por defecto para "topics" //course format: weeks, topics, social, site,..
    showgrades = 1 # Valor por defecto para "1" //1 if grades are shown, otherwise 0
    newsitems = 5 # Valor por defecto para "5" //number of recent items appearing on the course page

    showreports = 1 # Valor por defecto para "0" //are activity report shown (yes = 1, no =0)
    visible = 1 # Opcional //1: available to student, 0:not available
    groupmode = 0 # Valor por defecto para "0" //no group, separate, visible
    groupmodeforce = 0 # Valor por defecto para "0" //1: yes, 0: no
    return call('core_course_create_courses', courses=[{'fullname': u'%s' % fullname,
                                                        'shortname': shortname,
                                                        'categoryid': categoryid,
                                                        'idnumber': idnumber,
                                                        'summary': summary, 'format': format,
                                                        'showgrades': showgrades,
                                                        'newsitems': newsitems,
                                                        'startdate': startdate,
                                                        'enddate': enddate,
                                                        'numsections': numsections,
                                                        'maxbytes': maxbytes,
                                                        'showreports': showreports,
                                                        'visible': visible,
                                                        'groupmode': groupmode,
                                                        'groupmodeforce': groupmodeforce}])


######################################################################################################################
######################################################################################################################
# FUNCIONES PARA CREAR USUARIO
######################################################################################################################
######################################################################################################################
def BuscarUsuario( vkey, vvalue):
    """
    list of (
        object {
            key string   //the user column to search, expected keys (value format) are:
                        "id" (int) matching user id,
                        "lastname" (string) user last name (Note: you can use % for searching but it may be considerably slower!),
                        "firstname" (string) user first name (Note: you can use % for searching but it may be considerably slower!),
                        "idnumber" (string) matching user idnumber,
                        "username" (string) matching user username,
                        "email" (string) user email (Note: you can use % for searching but it may be considerably slower!),
                        "auth" (string) matching user auth plugin
            value string   //the value to search
        }
    )
    :param vkey:
    :param vvalue:
    :return:
    """
    return call('core_user_get_users', criteria=[{'key': vkey, 'value': vvalue}])


def EnrolarCurso( roleid, userid, courseid):
    """
    Roles definidos
    teacher => 3
    No edit Teacher => 4
    estudent => 5
    list of (
        object {
            roleid int   //Role to assign to the user
            userid int   //The user that is going to be enrolled
            courseid int   //The course to enrol the user role in

            timestart int  Opcional //Timestamp when the enrolment start
            timeend int  Opcional //Timestamp when the enrolment end
            suspend int  Opcional //set to 1 to suspend the enrolment
        }
    )
    :param roleid:
    :param userid:
    :param courseid:
    :return:
    """
    return call('enrol_manual_enrol_users',  enrolments=[{'roleid': roleid,
                                                         'userid': userid,
                                                         'courseid': courseid}])


def UnEnrolarCurso(roleid, userid, courseid):
    """
    Roles definidos
    teacher => 3
    No edit Teacher => 4
    estudent => 5
    list of (
        object {
            roleid int   //Role to assign to the user
            userid int   //The user that is going to be enrolled
            courseid int   //The course to enrol the user role in

            timestart int  Opcional //Timestamp when the enrolment start
            timeend int  Opcional //Timestamp when the enrolment end
            suspend int  Opcional //set to 1 to suspend the enrolment
        }
    )
    :param roleid:
    :param userid:
    :param courseid:
    :return:
    """
    return call('enrol_manual_unenrol_users', enrolments=[{'userid': userid,
                                                           'courseid': courseid,
                                                           'roleid': u'%s' % roleid}])


def EliminarUsuario(iduser):
    """
    list of (
    int   //user ID
    )
    :param iduser:
    :return:
    """
    return call('core_user_delete_users', userids=[iduser])


def CrearUsuario( username, password, firstname , lastname, email, idnumber , city, country):
    """
    Estructura general

    list of (
        object {
            username string   //Username policy is defined in Moodle security config.
            password string  Opcional //Plain text password consisting of any characters
            createpassword int  Opcional //True if password should be created and mailed to user.
            firstname string   //The first name(s) of the user
            lastname string   //The family name of the user
            email string   //A valid and unique email address
            idnumber string  Valor por defecto para "" //An arbitrary ID code number perhaps from the institution
            calendartype string  Valor por defecto para "gregorian" //Calendar type such as "gregorian", must exist on server
            theme string  Opcional //Theme name such as "standard", must exist on server
            timezone string  Opcional //Timezone code such as Australia/Perth, or 99 for default
            mailformat int  Opcional //Mail format code is 0 for plain text, 1 for HTML etc
            description string  Opcional //User profile description, no HTML
            city string  Opcional //Home city of the user
            country string  Opcional //Home country code of the user, such as AU or CZ
            firstnamephonetic string  Opcional //The first name(s) phonetically of the user
            lastnamephonetic string  Opcional //The family name phonetically of the user
            middlename string  Opcional //The middle name of the user
            alternatename string  Opcional //The alternate name of the user
            preferences  Opcional //User preferences
            list of (
                object {
                    type string   //The name of the preference
                    value string   //The value of the preference
                }
            )
            customfields  Opcional //User custom fields (also known as user profil fields)
            list of (
                object {
                    type string   //The name of the custom field
                    value string   //The value of the custom field
                }
            )
        }
    )
    :param username:
    :param password:
    :param firstname:
    :param lastname:
    :param email:
    :param idnumber:
    :param city:
    :param country:
    :return:
    """
    auth = 'manual' # Valor por defecto para "manual" //Auth plugins include manual, ldap, etc
    lang = 'es'  # Valor por defecto para "es" //Language code such as "en", must exist on server
    return call('core_user_create_users', users=[{'username': u'%s' % username,
                                                  'password': u'Gesti*%s' % password,
                                                  'firstname': firstname,
                                                  'idnumber': idnumber,
                                                  'lastname': lastname,
                                                  'email': email,
                                                  'city': city,
                                                  'country': country,
                                                  'auth': auth,
                                                  'lang': lang}])


