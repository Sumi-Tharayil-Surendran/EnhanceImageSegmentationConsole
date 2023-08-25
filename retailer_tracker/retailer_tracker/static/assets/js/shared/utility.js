(function () {
    if (!String.prototype.trim) {
        /**
         * Trim whitespace from each end of a String
         * @returns {String} the original String with whitespace removed from each end
         * @example
         * ' foo bar    '.trim(); //'foo bar'
         */
        String.prototype.trim = function trim() {
            return this.toString().replace(/^([\s]*)|([\s]*)$/g, '');
        };
    }
})();
const getCookie = (name) => {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const APIRequestHandlerFetch = (url, method, inputObject, successCallback) => {
    let options = {
        method: method,
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            'Content-Type': 'application/json',
            "X-Requested-With": "XMLHttpRequest"
        }
    }
    if (inputObject != null) {
        options.body = JSON.stringify(inputObject)
    }
    fetch(url, options)
        .then(response => response.json())
        .then((response) => {
            //console.log(response.json())
            successCallback(response)
        })
}

const APIRequestHandlerXMLHttpRequest = async (url, method, formData, successCallback) => {
    var xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhr.onprogress = function (pe) {
        if (pe.lengthComputable) {
            console.log(pe.total)
            console.log(pe.loaded)
        }
    }
    xhr.onloadend = function (pe) {
        console.log(pe.loaded)
        // do something to response
        console.log('completed')
        if (successCallback != null)
            successCallback(JSON.parse(this.responseText));
    }
    if (formData != null)
        xhr.send(formData);
    else
        xhr.send();
}
const IfNullReplace = (str, replace) => {
    if (str == null || str == undefined)
        return replace;
    else
        return str;


}
const setSelectByName = (element, text) => {
    const $select = element;
    const $options = Array.from($select.options);
    const optionToSelect = $options.find(item => item.text === text);
    optionToSelect.selected = true;

}
