--
-- Create model DemandeOuOffre
--
CREATE TABLE `mentoring_requests` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `type_publication` varchar(10) NOT NULL, `format_seance` varchar(15) NOT NULL, `description` longtext NOT NULL, `statut` varchar(10) NOT NULL, `date_creation` datetime(6) NOT NULL, `date_modification` datetime(6) NOT NULL, `auteur_id` bigint NOT NULL, `competence_id` bigint NOT NULL);
--
-- Create model Matching
--
CREATE TABLE `match_suggestions` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `score_global` numeric(5, 2) NOT NULL, `score_competences` numeric(5, 2) NOT NULL, `score_horaires` numeric(5, 2) NOT NULL, `score_filiere` numeric(5, 2) NOT NULL, `statut` varchar(15) NOT NULL, `date_creation` datetime(6) NOT NULL, `mentor_id` bigint NOT NULL, `mentore_id` bigint NOT NULL);
ALTER TABLE `mentoring_requests` ADD CONSTRAINT `mentoring_requests_auteur_id_832d8d77_fk_users_id` FOREIGN KEY (`auteur_id`) REFERENCES `users` (`id`);
ALTER TABLE `mentoring_requests` ADD CONSTRAINT `mentoring_requests_competence_id_da33323d_fk_skills_id` FOREIGN KEY (`competence_id`) REFERENCES `skills` (`id`);
ALTER TABLE `match_suggestions` ADD CONSTRAINT `match_suggestions_mentor_id_mentore_id_e6033301_uniq` UNIQUE (`mentor_id`, `mentore_id`);
ALTER TABLE `match_suggestions` ADD CONSTRAINT `match_suggestions_mentor_id_910f129b_fk_users_id` FOREIGN KEY (`mentor_id`) REFERENCES `users` (`id`);
ALTER TABLE `match_suggestions` ADD CONSTRAINT `match_suggestions_mentore_id_4a3e0fe4_fk_users_id` FOREIGN KEY (`mentore_id`) REFERENCES `users` (`id`);
