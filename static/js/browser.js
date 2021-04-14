{
    const app = Vue.createApp({
        delimiters: ['[[', ']]'],
        data() {
            return {
                loading: true,
                space_id: space_id,
                urls:{
                    browse: rootApiUrl,
                    addFolder: addFolderApiUrl,
                    addFile: addFileApiUrl,
                },
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

                current.full_path = `/${current.path.join('/')}`;
                return current
            },
            folderList() {
                let list = this.data.folders;
                list.forEach(function (folder, index) {
                    folder.created_on_display = moment(folder.created_on).fromNow();
                    folder.updated_on_display = moment(folder.updated_on).fromNow();
                    folder.created_on = moment(folder.created_on).format(defaultDateTimeFormat);
                    folder.updated_on = moment(folder.updated_on).format(defaultDateTimeFormat);
                    folder.size = folder.files_total_size ? humanFileSize(folder.files_total_size) : '';
                    folder.full_path = `/${folder.path.join('/')}`;
                })
                return list;
            },
            fileList() {
                let list = this.data.files;
                let current_folder = this.data.current_folder;
                let folder_path = current_folder?.full_path ?? '/';
                list.forEach(function (file, index) {
                    file.created_on_display = moment(file.created_on).fromNow();
                    file.updated_on_display = moment(file.updated_on).fromNow();
                    file.created_on = moment(file.created_on).format(defaultDateTimeFormat);
                    file.updated_on = moment(file.updated_on).format(defaultDateTimeFormat);
                    file.size = humanFileSize(file.content_length);
                    file.folder_path = folder_path;

                    file.children.forEach(function (childFile, index) {
                        childFile.created_on_display = moment(childFile.created_on).fromNow();
                        childFile.updated_on_display = moment(childFile.updated_on).fromNow();
                        childFile.created_on = moment(childFile.created_on).format(defaultDateTimeFormat);
                        childFile.updated_on = moment(childFile.updated_on).format(defaultDateTimeFormat);
                        childFile.size = humanFileSize(childFile.content_length);
                    });
                })
                return list;
            },
        },
        created() {
            this.loadData(this.urls.browse);
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
                this.loadData(folder?.url ?? this.urls.browse);
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
            refreshData (){
                this.loadData(this.data.current_folder?.url ?? this.urls.browse);
            },
            addFolder() {
                let $this = this;
                let folder_name = $this.data.current_folder? './' + $this.data.current_folder.name : 'Root';
                Swal.fire({
                    icon: 'question',
                    iconHtml: '<i class="ft-folder-plus"></i>',
                    title: `Add Folder To ${folder_name}`,
                    input: 'text',
                    inputAttributes: {
                        autocapitalize: 'off',
                        placeholder: 'Folder name'
                    },
                    showCancelButton: true,
                    confirmButtonText: 'Add',
                    showLoaderOnConfirm: true,
                    allowOutsideClick: () => !Swal.isLoading(),
                    preConfirm: (folder_name) => {
                        return axios.post($this.urls.addFolder, {
                            space: $this.space_id,
                            parent: $this.data.current_folder?.id ?? null,
                            name: folder_name
                        }).then(res => {
                            return res.data;
                        }).catch(handleSwalAxiosError);
                    },
                }).then((result) => {
                    if (!result || !result.isConfirmed) return;
                    $this.refreshData();
                    Swal.fire({
                        'icon': 'success',
                        'text': 'Added Folder'
                    });
                })
            },
            renameFolder(folder) {
                let $this = this;
                let folder_name = folder.name;
                Swal.fire({
                    icon: 'question',
                    iconHtml: '<i class="ft-folder"></i>',
                    title: 'Rename Folder',
                    inputValue: folder_name,
                    input: 'text',
                    inputAttributes: {
                        autocapitalize: 'off',
                        placeholder: 'Folder name'
                    },
                    showCancelButton: true,
                    confirmButtonText: 'Rename',
                    showLoaderOnConfirm: true,
                    allowOutsideClick: () => !Swal.isLoading(),
                    preConfirm: (folder_name) => {
                        return axios.patch(folder.update_url, {
                            name: folder_name
                        }).then(res => {
                            folder.name = res.data.name;
                            return res.data;
                        }).catch(handleSwalAxiosError);
                    },
                }).then((result) => {
                    if (!result || !result.isConfirmed) return;
                    $this.refreshData();
                    Swal.fire({
                        'icon': 'success',
                        'text': 'Renamed Folder'
                    });
                })
            },
            uploadFile(folder = null) {
                let $this = this;
                let folder_name = folder?.name ?? 'Root';

                Swal.fire({
                    icon: 'question',
                    iconHtml: '<i class="ft-file-plus"></i>',
                    title: `Upload file to ${folder_name} Folder`,
                    input: 'file',
                    inputAttributes: {
                        placeholder: 'Select File',
                        accept: '*',
                        'aria-label': 'Select file to upload'
                    },
                    showCancelButton: true,
                    confirmButtonText: 'Upload',
                    showLoaderOnConfirm: true,
                    allowOutsideClick: () => !Swal.isLoading(),
                    preConfirm: (file) => {
                        const formData = new FormData();
                        if(file) formData.append('content', file);
                        formData.append('space', $this.space_id);
                        if(!!folder){
                            formData.append('folder', folder?.id ?? null);
                        }

                        return axios.post($this.urls.addFile, formData, {
                            headers: {
                                'Content-Type': 'multipart/form-data',
                            }
                        }).then(res => {
                            return res.data;
                        }).catch(handleSwalAxiosError);
                    },
                }).then((result) => {
                    if (!result || !result.isConfirmed) return;
                    $this.refreshData();
                    Swal.fire({
                        'icon': 'success',
                        'text': 'Added File',
                    });
                })
            }
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
                    <div class="small font-weight-bold mt-1" :title="details.created_on">Added: [[ details.created_on_display ]]</div>
                    <div class="small font-weight-bold mt-1" :title="details.updated_on">Updated: [[ details.updated_on_display ]]</div>
                </div>
                <div class="col-12 mt-3">
                    <div class="small font-weight-bold mt-1">File name:</div>
                    <a :href="details.serve_url" target="_blank" class="text-700">[[ details.name ]]</a>
                </div>
                <div class="col-12 mt-3">
                    <div class="small font-weight-bold mt-1">Location:</div>
                    <a class="text-700">[[ details.folder_path ]]</a>
                </div>
                <div v-if="!!details.children.length" class="col-12 mt-3">
                    <div class="small font-weight-bold mt-1">Pipelines:</div>
                    <a v-for="child in details.children" :href="child.serve_url" target="_blank" class="text-700 d-block">
                        [[ child.pipeline.name ]] - <span :title="child.name">[[ child.short_name ]]</span> - [[ child.size ]]
                    </a>
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
                    <div class="small font-weight-bold mt-1" :title="details.created_on">Added: [[ details.created_on_display ]]</div>
                    <div class="small font-weight-bold mt-1" :title="details.updated_on">Updated: [[ details.updated_on_display ]]</div>
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
