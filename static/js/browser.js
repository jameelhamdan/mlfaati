{
    const app = Vue.createApp({
        delimiters: ['[[', ']]'],
        data() {
            return {
                loading: true,
                rootApiUrl: rootApiUrl,
                current_detail: null,
                data: {
                    current_folder: null,
                    folders: [],
                    files: [],
                },
            }
        },
        computed: {
            currentDetail() {
                return this.current_detail;
            },
            currentFolder(){
                let current = this.data.current_folder;
                if (!current) return null;

                if (current.ancestors.length > 0) {
                    current.previous = current.ancestors[current.ancestors.length - 1];
                } else {
                    current.previous = null;
                }
                return current
            },
            folderList() {
                let list = this.data.folders;
                list.forEach(function (folder, index) {
                    folder.created_on_display = moment(folder.created_on).fromNow();
                    folder.updated_on_display = moment(folder.updated_on).fromNow();
                    folder.created_on = moment(folder.created_on).format("YYYY-MM-DD HH:mm:ss");
                    folder.updated_on = moment(folder.updated_on).format("YYYY-MM-DD HH:mm:ss");
                    folder.size = folder.files_total_size ? humanFileSize(folder.files_total_size) : '';
                    folder.full_path = `/${folder.path.join('/')}`;
                })
                return list;
            },
            fileList() {
                let list = this.data.files;
                let current_folder = this.data.current_folder;
                let folder_path = `/${current_folder? current_folder.path.join('/'): ''}`;
                list.forEach(function (file, index) {
                    file.created_on_display = moment(file.created_on).fromNow();
                    file.updated_on_display = moment(file.updated_on).fromNow();
                    file.created_on = moment(file.created_on).format("YYYY-MM-DD HH:mm:ss");
                    file.updated_on = moment(file.updated_on).format("YYYY-MM-DD HH:mm:ss");
                    file.size = humanFileSize(file.content_length);
                    file.folder_path = folder_path;

                    list.forEach(function (childFile, index) {
                        childFile.created_on_display = moment(childFile.created_on).fromNow();
                        childFile.updated_on_display = moment(childFile.updated_on).fromNow();
                        childFile.created_on = moment(childFile.created_on).format("YYYY-MM-DD HH:mm:ss");
                        childFile.updated_on = moment(childFile.updated_on).format("YYYY-MM-DD HH:mm:ss");
                        childFile.size = humanFileSize(childFile.content_length);
                    });
                })
                return list;
            },
        },
        created() {
            this.loadData(this.rootApiUrl);
        },
        methods: {
            selectDetail(type, details) {
                this.unselectDetail();
                this.current_detail = {
                    type: type,
                    data: details,
                }
                this.current_detail.data.selected = true;
            },
            unselectDetail() {
                if(!!this.current_detail)
                    this.current_detail.data.selected = false;
                this.current_detail = null;
            },
            openFolder(folder = null) {
                this.unselectDetail();
                if (folder) {
                    this.loadData(folder.url);
                } else {
                    this.loadData(this.rootApiUrl);
                }
            },
            openFile(file) {
                window.open(file.serve_url, '_blank').focus();
            },
            loadData(url) {
                let $this = this;
                $this.loading = true;
                axios.get(url).then(res => {
                    $this.data = res.data;
                    $this.loading = false;
                });
            },
        }
    })

    app.component('file-details', {
        props: ['details'],
        delimiters: ['[[', ']]'],
        template: `
            <div class="row align-items-center">
                <div class="col-auto">
                    <a :href="details.serve_url" target="_blank" class="text-dark ft-6x ft-file"></a>
                </div>
                <div class="col">
                    <a><h3 class="h5">[[ details.content_type ]]</h3></a>
                    <div class="small font-weight-bold mt-1">Size: [[ details.size ]]</div>
                    <div class="small font-weight-bold mt-1" :title="details.created_on">Added on: [[ details.created_on_display ]]</div>
                    <div class="small font-weight-bold mt-1" :title="details.updated_on">Updated on: [[ details.updated_on_display ]]</div>
                </div>
                <div class="col-12 mt-3">
                    <div class="small font-weight-bold mt-1">File name:</div>
                    <a :href="details.serve_url" target="_blank" class="text-700">[[ details.name ]]</a>
                </div>
                <div class="col-12 mt-3">
                    <div class="small font-weight-bold mt-1">Location:</div>
                    <a class="text-700">[[ details.folder_path ]]</a>
                </div>
            </div>
        `
    });

    app.component('folder-details', {
        props: ['details'],
        delimiters: ['[[', ']]'],
        template: `
            <div class="row align-items-center">
                <div class="col-auto">
                    <a class="text-dark ft-6x ft-folder"></a>
                </div>
                <div class="col">
                    <a><h3 class="h5">[[ details.files_count ]] Files</h3></a>
                    <div class="small font-weight-bold mt-1">Total Size: [[ details.size ]]</div>
                    <div class="small font-weight-bold mt-1" :title="details.created_on">Added on: [[ details.created_on_display ]]</div>
                    <div class="small font-weight-bold mt-1" :title="details.updated_on">Updated on: [[ details.updated_on_display ]]</div>
                </div>
                <div class="col-12 mt-3">
                    <div class="small font-weight-bold mt-1">Folder name:</div>
                    <a class="text-700">[[ details.name ]]</a>
                </div>
                <div class="col-12 mt-3">
                    <div class="small font-weight-bold mt-1">Location:</div>
                    <a class="text-700">[[ details.full_path ]]</a>
                </div>
            </div>
        `
    });

    app.mount('#browserApp');
}
