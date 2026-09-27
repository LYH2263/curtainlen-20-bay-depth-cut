<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
</script>
<template><div class="page"><h1>记录</h1><ul><li v-for="r in items" :key="r.id">{{ r.window_name }} {{ r.result?.meters }}m（裁高 {{ r.result?.cut_height }}m<span v-if="r.result?.bay_enabled">，飘窗+{{ r.result?.bay_depth }}m</span>）</li></ul></div></template>
