'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('myApp.services', []).
    service('authState', function () {
        return {
            user: undefined
        };
    }).
  	value('version', '0.1').
  	value('Shared', function(){
  		var selectedSchool = undefined;
  		return {selectedSchool:selectedSchool};
  	})
