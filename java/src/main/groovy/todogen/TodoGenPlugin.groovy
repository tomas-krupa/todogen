package todogen

import org.gradle.api.GradleException
import org.gradle.api.Plugin
import org.gradle.api.Project
import org.gradle.api.tasks.Exec
import org.gradle.api.file.DirectoryProperty
import org.gradle.api.file.RegularFileProperty

class TodoGenPlugin implements Plugin<Project> {
    @Override
    void apply(Project p) {
        def ext = p.extensions.create('todogen', TodoGenExtension, p)

        def update = p.tasks.register('updateTodos', Exec) { Exec t ->
            t.group = 'documentation'
            t.description = 'Collect TODOs into README via embedded todogen.py'

            // Avoid hashing .gradle locks entirely
            t.doNotTrackState("External python; avoid scanning Gradle internals like .gradle/** lock files")

            // (Optional) still declare outputs so Gradle knows what is produced
            t.outputs.file(ext.readme)

            t.doFirst {
                if (!ext.srcDir.isPresent() || !ext.readme.isPresent()) {
                    throw new GradleException("todogen: 'srcDir' and 'readme' must be set in the 'todogen { ... }' block.")
                }

                // Copy embedded script to build/
                File target = new File(p.buildDir, "todogen/todogen.py")
                target.parentFile.mkdirs()
                InputStream inStream = this.class.getResourceAsStream('/dev/tomaskrupa/scripts/todogen.py') //TODO fix hgarcoded group
                if (inStream == null) throw new GradleException("todogen: embedded script not found at /dev/tomaskrupa/scripts/todogen.py") //TODO fix hgarcoded group
                try { target.bytes = inStream.bytes } finally { try { inStream.close() } catch (ignored) {} }
                target.setExecutable(true)

                File srcDirFile = ext.srcDir.get().asFile
                File readmeFile = ext.readme.get().asFile
                readmeFile.parentFile?.mkdirs()

                p.logger.lifecycle("Updating ${readmeFile} from ${srcDirFile}...")
                String exe = (String)(p.findProperty("todogenPython") ?: System.getenv("PYTHON")) ?: "python"

                t.executable = exe
                t.args = [
                    target.absolutePath,
                    '--readme', readmeFile.absolutePath,
                    '--src',    srcDirFile.absolutePath
                ]
            }
        }

        p.plugins.withId('base')  { p.tasks.named('build').configure { it.dependsOn(update) } }
        p.pluginManager.withPlugin('java') { p.tasks.named('build').configure { it.dependsOn(update) } }
    }
}

class TodoGenExtension {
    final DirectoryProperty srcDir
    final RegularFileProperty readme
    TodoGenExtension(Project p) {
        this.srcDir = p.objects.directoryProperty()
        this.readme = p.objects.fileProperty()
    }
}
