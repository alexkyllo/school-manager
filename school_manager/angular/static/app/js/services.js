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
  	}).
    factory('api', function($resource){
        function add_auth_header(data, headersGetter){
            var headers = headersGetter();
            headers['Authorization'] = ('Basic ' + btoa(data.username +
                                        ':' + data.password));
        }
        return {
            auth: $resource('/api/auth/login/', {}, {
                login:  {method: 'POST', transformRequest: add_auth_header},
                logout: {method: 'DELETE'}
            }),
            users: $resource('/api/users/:id/', {id:'@id'}, {}),
            schools: $resource('/api/schools/:id/', {id:'@id'}, {
                get: {method: 'GET', isArray: true}
            }),
            students: $resource('/api/students/:id/', {id:'@id'},{
                get: {method: 'GET', isArray: true}
            }),
            schoolStudents: $resource('/api/schools/:schoolId/students/', {schoolId:'@schoolId'},{
            	get: {method: 'GET', isArray: true}
            })
        };
    });
