(function() {
    var app = angular.module('GifsApp', []);

    app.controller('GifsController', ['$scope', '$http', function($scope, $http) {
        $scope.gifRows = [];
        $scope.search = '';

        var allGifs = [];

        $http.get('/gifs')
            .then(function (response) {
                $scope.gifRows = _.chunk(response.data.gifs, 4);
                allGifs = response.data.gifs;
            });

        $scope.filter = function () {
            var regex = new RegExp($scope.search, 'gi');

            if ($scope.search.length === 0) {
                $scope.gifRows = _.chunk(allGifs, 4);
                return;
            }

            $scope.gifRows = _.chunk(_.filter(allGifs, function(gif) {
                return regex.test(gif.title) || regex.test(gif.tags.join(' '));
            }), 4);
        };
    }]);
})();
