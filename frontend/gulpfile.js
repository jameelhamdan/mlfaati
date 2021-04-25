const gulp = require('gulp');
var plugins = require('gulp-load-plugins')();
plugins.del = require('del');

const TARGET_DIR = './static';

const paths = {
    dist: {
        vue: TARGET_DIR + '/vendor/vue',
        vendor: TARGET_DIR + '/vendor',
        css: TARGET_DIR + '/css',
    },
    src: {
        node_modules: './node_modules',
        scss: './src/scss',
    }
};

// Clean static file
gulp.task('clean', function(){
    return plugins.del([
        paths.dist.vue,
        paths.dist.vendor,
        paths.dist.css,
    ]);
});

// Copy node_modules to vendor
gulp.task('vendor', function () {
    return gulp.src([
        paths.src.node_modules + '/bootstrap/dist/js/bootstrap.bundle.min.js',
        paths.src.node_modules + '/onscreen/dist/on-screen.umd.js',
        paths.src.node_modules + '/smooth-scroll/dist/smooth-scroll.polyfills.min.js',
        paths.src.node_modules + '/moment/min/moment.min.js',
        paths.src.node_modules + '/sweetalert2/dist/sweetalert2.all.min.js',
        paths.src.node_modules + '/axios/dist/axios.min.js',
    ])
    .pipe(plugins.uglify())
    .pipe(plugins.concat('vendor.min.js'))
    .pipe(gulp.dest(paths.dist.vendor));

});

// Copy vue modules to vendor
gulp.task('vue', function () {
    return gulp.src([
        paths.src.node_modules + '/vue/dist/vue.global.prod.js',
    ])
    .pipe(gulp.dest(paths.dist.vue));
});

// Compile and copy scss/css
gulp.task('css', function () {
    return gulp.src([
        paths.src.scss + '/app/**/*.scss',
        paths.src.scss + '/custom/**/*.scss',
        paths.src.scss + '/app.scss'
    ])
    .pipe(plugins.wait(500))
    .pipe(plugins.sourcemaps.init())
    .pipe(plugins.sass().on('error', plugins.sass.logError))
    .pipe(plugins.autoprefixer({
        overrideBrowserslist: ['> 1%']
    }))
    .pipe(plugins.sourcemaps.write('.'))
    .pipe(gulp.dest(paths.dist.css));
});

gulp.task('build', gulp.series(
    'clean', 'vendor', 'vue', 'css'
));
