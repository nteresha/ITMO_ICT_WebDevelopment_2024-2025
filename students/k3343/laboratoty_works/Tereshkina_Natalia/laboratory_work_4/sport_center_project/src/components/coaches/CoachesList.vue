<template>
  <h2>Список всех тренеров</h2>
  <hr class="hr-1">
  <br>
  <CoachesAddNew />
  <br>
  <div class="main">
    <div class="coach-info" v-for="coach in coaches" :key="coach.id">
      <img v-if="coach.gender === 'f'" src="../../assets/images/coaches/coach-icon-f.png" />
      <img v-else src="../../assets/images/coaches/coach-icon-m.png" />
      <div class="coach-details">
        <div class="coach-full-information">
          <h3>{{ coach.last_name }} {{ coach.first_name }} {{ coach.middle_name }}</h3>
          <p>Дата рождения: {{ coach.date_of_birth }}</p>
          <p>Квалификация: {{ coach.qualification.toLowerCase() }}</p>
          <p>Опыт работы: {{ coach.experience }}</p>
          <hr class="hr-1">
        </div>
        <div class="coach-sections">
          <h4>Секции тренера</h4>
          <ul>
            <li v-for="section in coach.sections" :key="section.id" v-if="coach.sections.length>0">
              {{ section.title }}
            </li>
            <li v-else>
              Нет секций
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CoachesAddNew from "@/components/coaches/CoachesAddNew.vue";

export default {
  components: {
    CoachesAddNew,
  },
  data() {
    return {
      coaches: [],
    };
  },
  methods: {
    async fetchCoaches() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/coaches/");
        this.coaches = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке тренеров:", error);
      }
    },
  },
  mounted() {
    this.fetchCoaches();
  },
};
</script>

<style scoped>
h2 {
  margin-top: 2%;
}
.hr-1{
  border: none;
  background-color: midnightblue;
  height: 2px;
}

.main {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.coach-info {
  flex: 1 1 calc(33% - 40px);
  max-width: 500px;
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 2px solid midnightblue;
  border-radius: 20px;
  padding: 15px;
  text-align: center;
}

.coach-details {
  display: flex;
  flex-direction: column;
  align-items: center;
}

@media (max-width: 1200px) {
  .coach-info {
    flex: 1 1 calc(50% - 20px);
  }
}

@media (max-width: 768px) {
  .coach-info {
    flex: 1 1 100%;
  }
}

img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
}

h2 {
  text-align: center;
  color: midnightblue;
}

.coach-full-information {
  flex: 1;
}

.coach-sections {
  flex: 0 0 20%;
  padding: 10px;
}

.coach-details h1 {
  margin-bottom: 1%;
}

.coach-details p {
  color: #555555;
  margin: 0.5% 0;
}

.coach-sections ul {
  list-style-type: none;
  padding: 0;
}
</style>
