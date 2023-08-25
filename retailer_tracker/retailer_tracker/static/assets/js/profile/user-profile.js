var flImage = document.getElementById('flImage')
var imgProfileImage = document.getElementById('imgProfileImage')
addEventListener("DOMContentLoaded", (event) => {
    CandidateProfileBasicGet();
    const elems = document.querySelectorAll('.datepicker_input');
    for (const elem of elems) {
        const datepicker = new Datepicker(elem, {
            'format': 'yyyy-mm-dd', // UK format
            title: getDatePickerTitle(elem)
        });
    }

    flImage.onchange = evt => {
        const [file] = flImage.files
        if (file) {
            imgProfileImage.src = URL.createObjectURL(file)
        }
    }

});

document.getElementById('btnUpdateCandidateBasicDetails').addEventListener("click", (event) => {
    let obj = {};
    obj.first_name = document.getElementById('txtFirstName').value;
    obj.middle_name = document.getElementById('txtMiddleName').value;
    obj.last_name = document.getElementById('txtLastName').value;
    obj.about = document.getElementById('txtAbout').value;
    //const email = document.getElementById('txtEmail').value;
    obj.date_of_birth = document.getElementById('txtDateOfBirth').value;
    obj.passport = document.getElementById('txtPassport').value;
    obj.gender = document.getElementById('ddlGender').value;
    obj.nationality = document.getElementById('ddlNationality').value;
    obj.marital_status = document.getElementById('ddlMaritalStatus').value;
    obj.phone = document.getElementById('txtPhone').value;
    var formData = new FormData();
    if (flImage.files.length > 0)
        formData.append("profileImage", flImage.files[0]);
    formData.append("jsonData", JSON.stringify(obj));
    CandidateProfileBasicUpdate(formData)
})
document.getElementById('btnUploadProfileImage').addEventListener("click", (event) => {
    document.getElementById('flImage').click();
})
document.getElementById('btnUploadProfileImageRemove').addEventListener("click", (event) => {
    var newInput = document.createElement("input");
    newInput.type = "file";
    newInput.id = flImage.id;
    newInput.name = flImage.name;
    newInput.className = flImage.className;
    newInput.style.cssText = flImage.style.cssText;
    newInput.hidden = true
    flImage.replaceWith(flImage = newInput);
    flImage.onchange = evt => {
        const [file] = flImage.files
        if (file) {
            imgProfileImage.src = URL.createObjectURL(file)
        }
    }
    imgProfileImage.src = profile_image_default
})
document.getElementById('btnChangePassword').addEventListener("click", (event) => {
    const old_password = document.getElementById('txtCurrentPassword').value
    const new_password = document.getElementById('txtNewPassword').value
    const renew_password = document.getElementById('txtRenewPassword').value
    if (old_password == "" || new_password == "" || renew_password == "") {
        messsageModalShow("Alert", "Provide all the required details")
        return;
    }
    const obj = { 'old_password': old_password, 'new_password': new_password, 'renew_password': renew_password };
    CandidatePasswordUpdate(obj);
})

document.getElementById('btnSaveCandidateEducation').addEventListener("click", (event) => {
    let edObj = {}
    edObj.degree = document.getElementById('ddlDegree').value
    edObj.major = document.getElementById('txtMajor').value
    edObj.university = document.getElementById('txtUniversity').value
    edObj.country = document.getElementById('ddlCountry').value
    edObj.city = document.getElementById('ddlCity').value
    edObj.year = document.getElementById('txtYear').value
    edObj.gpa = document.getElementById('txtGPA').value
    if (edObj.degree == "" || edObj.major == "" || edObj.university == "" || edObj.country == "" ||
        edObj.city == "" || edObj.year == "" || edObj.gpa == "") {
        messsageModalShow("Alert", "Provide all the required details")
        return;
    }
    CandidateEducationAdd(edObj);
})
document.getElementById('ddlCountry').addEventListener("change", (event) => {
    const countryID = document.getElementById('ddlCountry').value
    if (countryID == "") {
        return;
    }
    const obj = { 'country_id': countryID };
    CitycGet(obj);
})




// tags
var input2 = document.querySelector('textarea[name=tags2]')
var tagify2 = new Tagify(input2, {
    enforeWhitelist: true,
    whitelist: [],
    callbacks: {
        // "change": (e) => console.log(e.detail),
        // "dropdown:show": (e) => console.log(e.detail),
        "add": (e) => {
            console.log('added:' + e.detail.data.value)
            var obj = {};
            obj.tag = e.detail.data.value
            CandidateSkillAdd(obj);

            // console.log(e.detail)
        },
        "remove": (e) => {
            console.log('removed:' + e.detail.data.value)
            var obj = {};
            obj.tag = e.detail.data.value
            CandidateSkillRemove(obj);
        }

    }
});




const getDatePickerTitle = elem => {
    // From the label or the aria-label
    const label = elem.nextElementSibling;
    let titleText = '';
    if (label && label.tagName === 'LABEL') {
        titleText = label.textContent;
    } else {
        titleText = elem.getAttribute('aria-label') || '';
    }
    return titleText;
}

const CandidateProfileBasicGet = async () => {
    APIRequestHandlerFetch(profile_basic_get, 'GET', null, (response) => {
        console.log(response.result)
        // console.log('success')
        const userInfo = response.result;
        LoadCandidateBasicDetails(userInfo)
    })
}
const LoadCandidateBasicDetails = (userInfo) => {
    const candiateName = IfNullReplace(userInfo.first_name, "") + " " + IfNullReplace(userInfo.middle_name, "") + " " + IfNullReplace(userInfo.last_name, "")
    imgProfileImage.src = IfNullReplace(userInfo.profile_image_path, profile_image_default)
    document.getElementById('imgProfileImageBig').src = IfNullReplace(userInfo.profile_image_path, profile_image_default)
    document.getElementById('pCandidateAbout').innerHTML = IfNullReplace(userInfo.about, "")
    document.getElementById('divCandidateFullName').innerHTML = candiateName;
    document.getElementById('hCandidateName').innerHTML = candiateName;
    document.getElementById('divEmail').innerHTML = IfNullReplace(userInfo.email, "")
    document.getElementById('divDataOfBirth').innerHTML = IfNullReplace(userInfo.date_of_birth, "")
    document.getElementById('divPassport').innerHTML = IfNullReplace(userInfo.passport, "")
    document.getElementById('divGender').innerHTML = IfNullReplace(userInfo.gender, "")
    document.getElementById('divNationality').innerHTML = IfNullReplace(userInfo.nationality, "")
    document.getElementById('divMaritalStatus').innerHTML = IfNullReplace(userInfo.marital_status, "")
    document.getElementById('divPhone').innerHTML = IfNullReplace(userInfo.phone, "")
    document.getElementById('txtFirstName').value = IfNullReplace(userInfo.first_name, "");
    document.getElementById('txtMiddleName').value = IfNullReplace(userInfo.middle_name, "")
    document.getElementById('txtLastName').value = IfNullReplace(userInfo.last_name, "");
    document.getElementById('txtAbout').value = IfNullReplace(userInfo.about, "")
    document.getElementById('txtDateOfBirth').value = IfNullReplace(userInfo.date_of_birth, "")
    document.getElementById('txtPassport').value = IfNullReplace(userInfo.passport, "")
    document.getElementById('txtPhone').value = IfNullReplace(userInfo.phone, "")
    setSelectByName(document.getElementById('ddlGender'), IfNullReplace(userInfo.gender, ""))
    setSelectByName(document.getElementById('ddlNationality'), IfNullReplace(userInfo.nationality, ""))
    setSelectByName(document.getElementById('ddlMaritalStatus'), IfNullReplace(userInfo.marital_status, ""))
}
const CandidateProfileBasicUpdate = async (userInfo) => {
    APIRequestHandlerXMLHttpRequest(profile_basic_update, 'post', userInfo, (response) => {
        console.log(response.result)
        const result = response.result;
        if (result.status == "success") {
            messsageModalShow("Info", "The candidate details have been saved")
            CandidateProfileBasicGet();
        }
        else {
            messsageModalShow("Alert", result.message)
        }
    })
}
const CandidatePasswordUpdate = async (data) => {
    APIRequestHandlerFetch(profile_password_update, 'POST', data, (response) => {
        console.log(response.result)
        // console.log('success')
        const result = response.result;
        if (result.status == "success") {
            messsageModalShow("Info", "The password has been updated successfully")
        }
        else {
            messsageModalShow("Alert", result.message)
        }
        //LoadCandidateBasicDetails(userInfo)

    })
}
const CandidateSkillAdd = async (data) => {
    APIRequestHandlerFetch(profile_skill_add, 'POST', data, (response) => {
        console.log(response.result)
        // console.log('success')
        const result = response.result;
        if (result.status == "success") {
            //messsageModalShow("Info", "The password has been updated successfully")
        }
        else {
            messsageModalShow("Alert", result.message)
        }
        //LoadCandidateBasicDetails(userInfo)

    })
}
const CandidateSkillRemove = async (data) => {
    APIRequestHandlerFetch(profile_skill_remove, 'POST', data, (response) => {
        console.log(response.result)
        // console.log('success')
        const result = response.result;
        if (result.status == "success") {
            //messsageModalShow("Info", "The password has been updated successfully")
        }
        else {
            messsageModalShow("Alert", result.message)
        }
        //LoadCandidateBasicDetails(userInfo)

    })
}
const CandidateEducationAdd = async (dataIInput) => {
    APIRequestHandlerFetch(profile_education_add, 'POST', dataIInput, (response) => {
        console.log(response.result)
        const result = response.result;
        if (result.status == "success") {
            const data = result.message
            const count = document.querySelectorAll('#tblEducation tbody tr').length

            //messsageModalShow("Info", "The password has been updated successfully")
            let tbodyRef = document.getElementById('tblEducation').getElementsByTagName('tbody')[0];
            tbodyRef.innerHTML += "<tr><th scope='row'>" + (count+1) + "</th><td>" + data.degree + "</td><td>" + data.major + "</td><td>" + data.university + "</td><td>" + data.city
                + "</td><td>" + data.country + "</td><td>" + data.year + "</td><td>"
                + data.gpa + "</td></tr>"

            // Insert a row at the end of table
            // let newRow = tbodyRef.insertRow();

            // // Insert a cell at the end of the row
            // let newCell = newRow.insertCell();
            // let newText = document.createTextNode(result.message.degree);

            //  newCell = newRow.insertCell();
            //  newText = document.createTextNode(result.message.degree);
            // newCell.appendChild(newText);
        }
        else {
            messsageModalShow("Alert", result.message)
        }
        //LoadCandidateBasicDetails(userInfo)

    })
}
const CandidateEducationRemove = async (data) => {
    APIRequestHandlerFetch(profile_education_remove, 'POST', data, (response) => {
        console.log(response.result)
        const result = response.result;
        if (result.status == "success") {
            //messsageModalShow("Info", "The password has been updated successfully")
        }
        else {
            messsageModalShow("Alert", result.message)
        }
        //LoadCandidateBasicDetails(userInfo)

    })
}
const CitycGet = async (data) => {
    APIRequestHandlerFetch(profile_city_get, 'POST', data, (response) => {
        console.log(response.result)
        // console.log('success')
        const cityList = response.result;
        const elem = document.getElementById('ddlCity')
        elem.innerHTML = "";
        cityList.forEach((v, i) => {
            elem.innerHTML += "<option value='" + v.id + "'>" + v.name + "</option>"

        })

    })
}
