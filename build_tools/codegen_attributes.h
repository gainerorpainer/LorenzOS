#pragma once

// Marks a function to be executed by LorenzOS with a given interval
#define task_with_interval(interval_ms) maybe_unused
// Marks a function to be called when the LorenzOS server is queried by the given ressource string
#define http_server_bind_to(ressource) maybe_unused
// marks a class to be serializable by LorenzOS into JSON. Give a SERIALIZABLE_ constant to specify access
#define is_serializable_class(acess) maybe_unused
// when passed to is_serializable_class(), marks that class to be serialized and parsed
#define SERIALIZABLE_AND_PARSABLE 0
// when passed to is_serializable_class(), marks that class to be only serialized
#define SERIALIZABLE_NO_PARSING 1
// marks a function to be executed by LorenzOS after the given classname is serialized
#define serialization_extension_for(classname) maybe_unused
// marks a function to be executed by LorenzOS after the given classname is parsed
#define parsing_extension_for(classname) maybe_unused