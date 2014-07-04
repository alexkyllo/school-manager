'use strict';

/* Controllers */

angular.module('myApp.controllers', [])
  .controller('userSchoolsCtrl', ['$scope', function($scope){
    $scope.schools = [
      {'name': 'A Cool School', 'id': 1}
    ]
  }])
  .controller('CalendarCtrl', ['$scope', function($scope) {

  }])
  .controller('StudentListCtrl', function($scope, api, Shared) {
  	$scope.students = api.students.get(function(data){
        return data.students;
    });
  })
  .controller('authController', function($scope, api, authState) {
        
        //$('#id_auth_form input').checkAndTriggerAutoFillEvent();

        $scope.authState = authState;
        $scope.selectedSchool = undefined;

        $scope.getCredentials = function(){
            return {username: $scope.username, password: $scope.password};
        };
        $scope.login = function(){
            api.auth.login($scope.getCredentials()).
                $promise.
                    then(function(data){
                        authState.user = data.username;
                    }).
                    catch(function(data){
                        alert(data.data.detail);
                    });
        };
        $scope.logout = function(){
            api.auth.logout(function(){
                authState.user = undefined;
            });
        };
        $scope.register = function($event){
            $event.preventDefault();
            api.users.create($scope.getCredentials()).
                $promise.
                    then($scope.login).
                    catch(function(data){
                        alert(data.data.username);
                    });
        };
        $scope.schools = api.schools.get(function(data){
            return data.schools;
        });
    });
