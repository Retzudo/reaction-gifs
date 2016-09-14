(function() {
    "use strict";

    var app = angular.module('GifsApp', ['gifPreview']);

    app.controller('GifsController', ['$scope', '$http', function($scope, $http) {
        $scope.gifs = [];
        $scope.search = '';

        $http.get('/gifs.json').then(function (response) {
            //$scope.gifs = response.data.gifs;
            $scope.gifs = response.data.gifs.map(function (gif) {
                gif.preview = '/preview/' + gif.url;
                gif.cached = '/gif/' + gif.url;
                return gif;
            });
        });
    }]);
}());
