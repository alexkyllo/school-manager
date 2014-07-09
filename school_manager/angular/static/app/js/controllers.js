'use strict';

/* Controllers */

angular.module('myApp.controllers', [])
  .controller('userSchoolsCtrl', function($scope, api, Shared){
    $scope.Shared = Shared;
    $scope.schools = api.schools.get(function(data){
            return data.schools;
        });
  })
  .controller('CalendarCtrl', ['$scope', function($scope) {

  }])
  .controller('StudentListCtrl', function($scope, api, Shared) {
      $scope.Shared = Shared;
      $scope.getStudents = function(){
        api.schoolStudents.get({schoolId : Shared.selectedSchool.id}).
        $promise.then(
          function(data){
            $scope.students = data;
          }
        )
      }
      $scope.$watch('Shared.selectedSchool', function() {
        $scope.getStudents();
      });
  })
  .controller('authController', function($scope, api, authState, Shared) {
        
        //$('#id_auth_form input').checkAndTriggerAutoFillEvent();

        $scope.authState = authState;
        $scope.Shared = Shared;

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
    });
